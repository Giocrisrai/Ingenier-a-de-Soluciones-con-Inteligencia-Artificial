# File: RA1/IL1.4/1-evaluation-rag.py
import streamlit as st
import os
import re
import json
import sys
import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

# LangChain imports
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# Streamlit: set_page_config debe ser la primera llamada st.*
st.set_page_config(page_title="RAG Evaluation", page_icon="📊", layout="wide")

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    st.warning("⚠️ python-dotenv no está instalado. Instálalo con: pip install python-dotenv")

# -----------------------------------------------------------------------------
# Configuración didáctica — modelos y URL (para que vean cómo se nombran en código)
# GitHub Models suele usar los mismos identificadores que la API de OpenAI.
# Cambien estos strings si el proveedor o el catálogo usan otros nombres.
# -----------------------------------------------------------------------------
API_BASE_URL_PREDETERMINADA = "https://models.inference.ai.azure.com"

# Modelo para chat / evaluaciones (client.chat.completions)
MODELO_CHAT = "gpt-4o"
# Alternativas frecuentes en catálogos compatibles: "gpt-4o-mini", "o1", etc.

# Modelo para embeddings (OpenAIEmbeddings de LangChain)
MODELO_EMBEDDINGS = "text-embedding-3-small"
# Otras opciones típicas: "text-embedding-3-large", "text-embedding-ada-002"

# Nombres usados en el resto del archivo (alias claros para el curso)
CHAT_MODEL = MODELO_CHAT
EMBEDDING_MODEL = MODELO_EMBEDDINGS

# Credenciales y host: desde .env (igual que en los notebooks IL1.2 / IL1.3)
github_token = os.getenv("GITHUB_TOKEN")
github_base_url = (
    os.getenv("OPENAI_BASE_URL")
    or os.getenv("GITHUB_BASE_URL")
    or API_BASE_URL_PREDETERMINADA
)

if github_token:
    os.environ["OPENAI_API_KEY"] = github_token
    os.environ["OPENAI_BASE_URL"] = github_base_url
# Sin token: no usar st.stop() aquí — impediría definir funciones; main() muestra el aviso.

logger = logging.getLogger("evaluation_rag")
_LOG_FILE = Path(__file__).resolve().parent / "1-evaluation-rag.run.log"


def configure_logging():
    """Consola (INFO+) y archivo (DEBUG+) en RA1/IL1.4/1-evaluation-rag.run.log"""
    if logger.handlers:
        return
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-5s | %(message)s",
        datefmt="%H:%M:%S",
    )
    sh = logging.StreamHandler(sys.stderr)
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    fh = logging.FileHandler(_LOG_FILE, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.info("Logging activo → consola + %s", _LOG_FILE)


def initialize_client():
    if not github_token:
        logger.warning("initialize_client: sin GITHUB_TOKEN")
        st.error("❌ No hay token de GitHub disponible.")
        return None
    
    logger.debug("OpenAI client base_url=%s", github_base_url)
    client = OpenAI(
        base_url=github_base_url,
        api_key=github_token
    )
    logger.info("Cliente OpenAI inicializado")
    return client

def initialize_embeddings():
    """Initialize LangChain embeddings model"""
    if not github_token:
        logger.warning("initialize_embeddings: sin token")
        st.error("❌ Se necesita GITHUB_TOKEN para inicializar embeddings.")
        return None
    
    try:
        logger.info("Inicializando OpenAIEmbeddings model=%s", EMBEDDING_MODEL)
        t0 = time.monotonic()
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        logger.info("OpenAIEmbeddings listo en %.2fs", time.monotonic() - t0)
        return embeddings
    except Exception as e:
        logger.exception("Fallo al inicializar embeddings: %s", e)
        st.error(f"Error al inicializar embeddings: {e}")
        return None

def _parse_score_1_to_10(text):
    """Extrae el primer número 1–10 del texto del modelo (evita fallos si añade texto)."""
    if not text:
        return None
    m = re.search(r"\b(10|[1-9])\b", text.strip())
    if m:
        return float(m.group(1))
    try:
        return float(text.strip().split()[0])
    except (ValueError, IndexError):
        return None


def get_embeddings_langchain(embeddings_model, texts):
    """Get embeddings using LangChain"""
    try:
        if not texts:
            logger.warning("embed_documents: lista vacía")
            st.error("No hay textos para embedir.")
            return None
        n = len(texts)
        logger.info("embed_documents: inicio (%d fragmentos)", n)
        t0 = time.monotonic()
        # Convert texts to LangChain Document objects if needed
        if isinstance(texts[0], str):
            documents = [Document(page_content=text) for text in texts]
        else:
            documents = texts
        
        # Get embeddings using LangChain
        embeddings = embeddings_model.embed_documents([doc.page_content for doc in documents])
        dt = time.monotonic() - t0
        arr = np.array(embeddings)
        logger.info("embed_documents: OK shape=%s en %.2fs", arr.shape, dt)
        return arr
    except Exception as e:
        logger.exception("embed_documents: error %s", e)
        st.error(f"Error al obtener embeddings: {e}")
        return None

def get_query_embedding_langchain(embeddings_model, query):
    """Get query embedding using LangChain"""
    try:
        qprev = (query[:120] + "…") if len(query) > 120 else query
        logger.debug("embed_query: %r", qprev)
        t0 = time.monotonic()
        embedding = embeddings_model.embed_query(query)
        logger.debug("embed_query: OK en %.2fs", time.monotonic() - t0)
        return np.array(embedding)
    except Exception as e:
        logger.exception("embed_query: error %s", e)
        st.error(f"Error al obtener embedding de la consulta: {e}")
        return None

def evaluate_faithfulness(client, query, context, response):
    if not client:
        return 5.0
        
    eval_prompt = f"""Evalúa si la respuesta es fiel al contexto proporcionado.

Consulta: {query}

Contexto:
{context}

Respuesta:
{response}

¿La respuesta está basada únicamente en la información del contexto? 
Responde con un número del 1-10 donde:
- 1-3: Respuesta contradice o no está basada en el contexto
- 4-6: Respuesta parcialmente basada en el contexto
- 7-10: Respuesta completamente fiel al contexto

Responde SOLO con el número:"""

    try:
        logger.debug("evaluate_faithfulness: llamada API chat model=%s", CHAT_MODEL)
        t0 = time.monotonic()
        result = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.1,
            max_tokens=10,
        )
        raw = result.choices[0].message.content or ""
        parsed = _parse_score_1_to_10(raw)
        score = parsed if parsed is not None else 5.0
        logger.info("evaluate_faithfulness: score=%.1f (raw=%r) en %.2fs", score, raw[:80], time.monotonic() - t0)
        return score
    except Exception as e:
        logger.warning("evaluate_faithfulness: fallo API → default 5.0 (%s)", e)
        return 5.0

def evaluate_relevance(client, query, response):
    if not client:
        return 5.0
        
    eval_prompt = f"""Evalúa qué tan relevante es la respuesta para la consulta.

Consulta: {query}

Respuesta: {response}

¿Qué tan bien responde la respuesta a la consulta?
Responde con un número del 1-10 donde:
- 1-3: Respuesta no relacionada o irrelevante
- 4-6: Respuesta parcialmente relevante
- 7-10: Respuesta muy relevante y útil

Responde SOLO con el número:"""

    try:
        logger.debug("evaluate_relevance: llamada API")
        t0 = time.monotonic()
        result = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.1,
            max_tokens=10,
        )
        raw = result.choices[0].message.content or ""
        parsed = _parse_score_1_to_10(raw)
        score = parsed if parsed is not None else 5.0
        logger.info("evaluate_relevance: score=%.1f en %.2fs", score, time.monotonic() - t0)
        return score
    except Exception as e:
        logger.warning("evaluate_relevance: fallo → 5.0 (%s)", e)
        return 5.0

def evaluate_context_precision(client, query, retrieved_docs):
    if not client or not retrieved_docs:
        return 0.0
    
    relevant_count = 0
    logger.info("evaluate_context_precision: %d documentos (1 llamada API c/u)", len(retrieved_docs))
    for di, doc in enumerate(retrieved_docs):
        eval_prompt = f"""¿Este documento es relevante para responder la consulta?

Consulta: {query}

Documento: {doc['document'][:300]}...

Responde SOLO 'SI' o 'NO':"""
        
        try:
            t0 = time.monotonic()
            result = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=[{"role": "user", "content": eval_prompt}],
                temperature=0.1,
                max_tokens=5,
            )
            raw_ans = (result.choices[0].message.content or "").strip()
            ok = bool(re.match(r"^(sí|si)\b", raw_ans, re.IGNORECASE))
            if ok:
                relevant_count += 1
            logger.debug(
                "context_precision doc %d/%d: %s (resp=%r, %.2fs)",
                di + 1,
                len(retrieved_docs),
                "SI" if ok else "NO",
                raw_ans[:40],
                time.monotonic() - t0,
            )
        except Exception as ex:
            logger.debug("context_precision doc %d: error %s", di, ex)
    
    ratio = relevant_count / len(retrieved_docs)
    logger.info("evaluate_context_precision: resultado=%.2f (%d relevantes)", ratio, relevant_count)
    return ratio

def hybrid_search_with_metrics(query, documents, embeddings, embeddings_model, top_k=5):
    start_time = time.time()
    qprev = (str(query)[:80] + "…") if len(str(query)) > 80 else str(query)
    logger.info("hybrid_search: inicio query=%r top_k=%d docs=%d", qprev, top_k, len(documents))

    if not query or not str(query).strip():
        logger.warning("hybrid_search: consulta vacía")
        return [], 0.0
    if not documents:
        logger.warning("hybrid_search: sin documentos")
        return [], 0.0
    emb_matrix = np.asarray(embeddings)
    if emb_matrix.ndim != 2 or emb_matrix.shape[0] != len(documents):
        logger.error(
            "hybrid_search: shape embeddings %s != %d documentos",
            emb_matrix.shape,
            len(documents),
        )
        st.error(
            "Los embeddings no coinciden con la lista de documentos. "
            "Genera de nuevo los embeddings en la pestaña Consulta."
        )
        return [], 0.0
    
    # Use LangChain for query embedding
    query_embedding = get_query_embedding_langchain(embeddings_model, query)
    if query_embedding is None:
        logger.error("hybrid_search: falló embedding de consulta")
        return [], 0.0
    
    semantic_similarities = cosine_similarity([query_embedding], emb_matrix)[0]
    
    keyword_scores = []
    query_words = set(query.lower().split())
    for doc in documents:
        doc_words = set(doc.lower().split())
        overlap = len(query_words.intersection(doc_words))
        keyword_scores.append(overlap / max(len(query_words), 1))
    
    combined_scores = 0.7 * semantic_similarities + 0.3 * np.array(keyword_scores)
    k = min(top_k, len(documents))
    top_indices = np.argsort(combined_scores)[::-1][:k]
    
    results = []
    for idx in top_indices:
        results.append({
            'document': documents[idx],
            'semantic_score': semantic_similarities[idx],
            'keyword_score': keyword_scores[idx],
            'combined_score': combined_scores[idx],
            'index': idx
        })
    
    retrieval_time = time.time() - start_time
    logger.info(
        "hybrid_search: OK %d resultados índices=%s en %.2fs",
        len(results),
        [r["index"] for r in results],
        retrieval_time,
    )
    return results, retrieval_time

def generate_response_with_metrics(client, query, context_docs):
    if not client:
        return "Error: cliente no disponible.", 0.0
        
    start_time = time.time()
    
    context = "".join([f"Documento {i+1}: {doc['document']}" 
                          for i, doc in enumerate(context_docs)])
    
    prompt = f"""Contexto:
{context}

Pregunta: {query}

Responde basándote únicamente en el contexto proporcionado."""

    try:
        logger.info(
            "generate_response: chat model=%s context_chars=%d",
            CHAT_MODEL,
            len(context),
        )
        t_api = time.monotonic()
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600,
        )
        
        generation_time = time.time() - start_time
        response_text = response.choices[0].message.content or ""
        logger.info(
            "generate_response: OK %d chars (API %.2fs, total %.2fs)",
            len(response_text),
            time.monotonic() - t_api,
            generation_time,
        )
        return response_text, generation_time
    except Exception as e:
        logger.exception("generate_response: error %s", e)
        return f"Error al generar respuesta: {e}", time.time() - start_time

def create_evaluation_dataset():
    return [
        {
            "query": "¿Qué es la inteligencia artificial?",
            "expected_context": "definición de IA",
            "ground_truth": "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana."
        },
        {
            "query": "¿Cómo funciona RAG?",
            "expected_context": "funcionamiento de RAG",
            "ground_truth": "RAG combina la búsqueda de información relevante con la generación de texto para producir respuestas más precisas."
        },
        {
            "query": "¿Qué es LangChain?",
            "expected_context": "descripción de LangChain",
            "ground_truth": "LangChain es un framework que facilita el desarrollo de aplicaciones con modelos de lenguaje."
        }
    ]

def log_interaction(query, response, metrics, context_docs):
    if 'interaction_logs' not in st.session_state:
        st.session_state.interaction_logs = []
    
    log_entry = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'query': query,
        'response': response,
        'metrics': metrics,
        'context_count': len(context_docs),
        'context_scores': [doc.get('combined_score', 0) for doc in context_docs]
    }
    
    st.session_state.interaction_logs.append(log_entry)

def export_langsmith_format(logs):
    langsmith_data = []
    for log in logs:
        langsmith_data.append({
            "run_id": log['id'],
            "timestamp": log['timestamp'],
            "inputs": {"query": log['query']},
            "outputs": {"response": log['response']},
            "metrics": log['metrics'],
            "metadata": {
                "context_count": log['context_count'],
                "context_scores": log['context_scores']
            }
        })
    return langsmith_data


def _truncate_for_csv(text: str, limit: int = 100) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def main():
    configure_logging()
    logger.info("======== main() ejecución Streamlit ========")

    st.title("📊 RAG con Evaluación y Monitoreo (LangChain)")
    st.caption(
        f"Modelos (editar arriba en el script: `MODELO_CHAT`, `MODELO_EMBEDDINGS`): "
        f"chat `{CHAT_MODEL}` · embeddings `{EMBEDDING_MODEL}` · API `{github_base_url}`"
    )
    st.write("Sistema RAG con métricas detalladas usando LangChain para embeddings.")

    with st.sidebar:
        st.header("📋 Monitoreo")
        st.caption(
            "Los eventos se escriben en la **consola** donde corre Streamlit "
            "y en el archivo de registro (nivel DEBUG en archivo)."
        )
        st.code(str(_LOG_FILE), language="text")
        if _LOG_FILE.exists():
            st.caption(f"Tamaño log: {_LOG_FILE.stat().st_size / 1024:.1f} KB")
    
    if not github_token:
        st.error("❌ Falta GITHUB_TOKEN. Revisa tu archivo `.env` en la raíz del proyecto.")
        st.info("💡 Copia `.env.example` a `.env` y define `GITHUB_TOKEN` con tu token de GitHub Models.")
        return
    
    if "eval_rag" not in st.session_state:
        st.session_state.eval_rag = {
            'documents': [
                "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana.",
                "Los modelos de lenguaje grande (LLM) son sistemas de IA entrenados en enormes cantidades de texto para generar y comprender lenguaje natural.",
                "RAG (Retrieval-Augmented Generation) combina la búsqueda de información relevante con la generación de texto para producir respuestas más precisas.",
                "LangChain es un framework que facilita el desarrollo de aplicaciones con modelos de lenguaje, proporcionando herramientas para cadenas y agentes.",
                "El prompt engineering es la práctica de diseñar instrucciones efectivas para obtener los mejores resultados de los modelos de IA.",
                "Los embeddings son representaciones vectoriales de texto que capturan el significado semántico en un espacio multidimensional.",
                "La búsqueda semántica utiliza embeddings para encontrar contenido relacionado por significado, no solo por palabras clave.",
                "Los sistemas de evaluación de IA miden métricas como relevancia, fidelidad y precisión del contexto."
            ],
            'embeddings': None,
            'embeddings_model': None,
            'enable_logging': True
        }
    
    if 'interaction_logs' not in st.session_state:
        st.session_state.interaction_logs = []
    
    client = initialize_client()
    if not client:
        st.error("❌ No se pudo inicializar el cliente OpenAI (revisa token y URL base).")
        return
    
    # Initialize LangChain embeddings model
    if st.session_state.eval_rag['embeddings_model'] is None:
        try:
            st.session_state.eval_rag['embeddings_model'] = initialize_embeddings()
        except Exception as e:
            st.error(f"Error inicializando embeddings: {str(e)}")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Consulta", "📄 Documentos", "📊 Métricas", "🧪 Evaluación", "📈 Analytics"])
    
    with tab1:
        st.header("💬 Consulta con Monitoreo (LangChain)")
        st.info(
            "Al **consultar** o **evaluar** verás un panel de progreso por pasos. "
            "Si activas *Evaluación automática*, el paso final hace varias llamadas al modelo "
            "y puede tardar más; la app sigue trabajando (revisa el panel o la terminal)."
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input("Haz tu pregunta:")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                top_k = st.slider("Docs a recuperar:", 1, 8, 3)
            with col_b:
                eval_enabled = st.checkbox("Evaluación automática", value=True)
            with col_c:
                st.session_state.eval_rag['enable_logging'] = st.checkbox("Logging", value=True)
        
        with col2:
            if st.button("🔄 Generar Embeddings (LangChain)"):
                logger.info("UI: clic Generar Embeddings")
                if st.session_state.eval_rag['documents'] and st.session_state.eval_rag['embeddings_model']:
                    nd = len(st.session_state.eval_rag['documents'])
                    with st.status(
                        f"⏳ Generando embeddings ({nd} textos)…",
                        expanded=True,
                    ) as emb_status:
                        st.markdown(
                            f"Enviando **{nd}** fragmentos al modelo **`{EMBEDDING_MODEL}`** "
                            "(una petición por lote a la API). Esto puede tardar decenas de segundos."
                        )
                        embeddings = get_embeddings_langchain(
                            st.session_state.eval_rag['embeddings_model'],
                            st.session_state.eval_rag['documents'],
                        )
                        if embeddings is not None:
                            st.session_state.eval_rag['embeddings'] = embeddings
                            st.markdown(f"✅ Vector listo: forma **{embeddings.shape}**")
                            emb_status.update(
                                label="✅ Embeddings generados",
                                state="complete",
                                expanded=False,
                            )
                            st.toast("Embeddings listos. Ya puedes consultar.", icon="✅")
                        else:
                            emb_status.update(
                                label="❌ Error al generar embeddings",
                                state="error",
                                expanded=True,
                            )
                            st.error("❌ Error generando embeddings")
                else:
                    st.warning("Modelo de embeddings no disponible")
        
        if st.button("🚀 Consultar con Métricas") and query:
            logger.info("UI: clic Consultar con Métricas eval=%s", eval_enabled)
            if st.session_state.eval_rag['embeddings'] is None:
                logger.warning("UI: consulta sin embeddings previos")
                st.warning("Genera embeddings primero")
            elif st.session_state.eval_rag['embeddings_model'] is None:
                logger.warning("UI: embeddings_model es None")
                st.warning("Modelo de embeddings no inicializado")
            else:
                results = None
                response = None
                metrics = None

                with st.status(
                    "⏳ Procesando tu consulta…",
                    expanded=True,
                ) as run_status:
                    st.caption("No cierres la pestaña: cada paso llama a la API y puede demorar.")

                    st.markdown("**Paso 1/3 — Recuperación** · Embedding de tu pregunta y ranking híbrido…")
                    results, retrieval_time = hybrid_search_with_metrics(
                        query,
                        st.session_state.eval_rag['documents'],
                        st.session_state.eval_rag['embeddings'],
                        st.session_state.eval_rag['embeddings_model'],
                        top_k,
                    )

                    if not results:
                        logger.error("UI: hybrid_search devolvió 0 resultados")
                        run_status.update(
                            label="❌ Sin documentos recuperados",
                            state="error",
                            expanded=True,
                        )
                        st.error("No se pudo recuperar documentos (revisa embeddings o la consulta).")
                    else:
                        st.markdown(
                            f"✅ **{len(results)}** documentos en **{retrieval_time:.2f}s**"
                        )

                        st.markdown(
                            f"**Paso 2/3 — Generación** · Modelo **`{CHAT_MODEL}`** con el contexto recuperado…"
                        )
                        logger.info("UI: generando respuesta (%d docs contexto)", len(results))
                        response, generation_time = generate_response_with_metrics(client, query, results)

                        metrics = {
                            'retrieval_time': retrieval_time,
                            'generation_time': generation_time,
                            'total_time': retrieval_time + generation_time,
                            'docs_retrieved': len(results),
                            'avg_relevance_score': np.mean([r['combined_score'] for r in results]),
                        }
                        st.markdown(f"✅ Respuesta en **{generation_time:.2f}s**")

                        if eval_enabled:
                            context_text = "".join([r['document'] for r in results])
                            n_extra = 2 + len(results)
                            st.markdown(
                                f"**Paso 3/3 — Evaluación de calidad** · "
                                f"≈ **{n_extra}** llamadas al chat (fidelidad, relevancia y "
                                f"{len(results)} juicios Sí/No por documento). **Puede tardar.**"
                            )
                            logger.info("UI: inicio evaluación automática (métricas LLM)")
                            metrics['faithfulness'] = evaluate_faithfulness(
                                client, query, context_text, response
                            )
                            metrics['relevance'] = evaluate_relevance(client, query, response)
                            metrics['context_precision'] = evaluate_context_precision(
                                client, query, results
                            )
                            logger.info("UI: fin evaluación automática")
                            st.markdown(
                                f"✅ Métricas listas (fidelidad **{metrics['faithfulness']:.1f}**, "
                                f"relevancia **{metrics['relevance']:.1f}**)"
                            )
                        else:
                            st.markdown("*Evaluación automática desactivada — se omitió el paso 3.*")

                        run_status.update(
                            label="✅ Consulta completada — resultado abajo",
                            state="complete",
                            expanded=False,
                        )
                        st.toast("Listo: revisa documentos y respuesta debajo.", icon="✅")

                if results and metrics is not None:
                    st.subheader("📋 Documentos Recuperados")
                    for i, result in enumerate(results):
                        with st.expander(f"Doc {i+1} - Score: {result['combined_score']:.3f}"):
                            st.write(result['document'])

                    st.subheader("🤖 Respuesta")
                    st.write(response)

                    st.subheader("⏱️ Métricas de Rendimiento")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Tiempo total", f"{metrics['total_time']:.2f}s")
                    with col2:
                        st.metric("Recuperación", f"{metrics['retrieval_time']:.2f}s")
                    with col3:
                        st.metric("Generación", f"{metrics['generation_time']:.2f}s")
                    with col4:
                        st.metric("Docs recuperados", metrics['docs_retrieved'])

                    if eval_enabled:
                        st.subheader("🎯 Métricas de Calidad")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Fidelidad", f"{metrics['faithfulness']:.1f}/10")
                        with col2:
                            st.metric("Relevancia", f"{metrics['relevance']:.1f}/10")
                        with col3:
                            st.metric("Precisión contexto", f"{metrics['context_precision']:.2f}")

                    if st.session_state.eval_rag['enable_logging']:
                        log_interaction(query, response, metrics, results)
                        logger.info("UI: interacción guardada en session logs")
    
    with tab2:
        st.header("📄 Gestión de Documentos")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📚 Documentos Actuales")
            
            # Display current documents with edit/delete options
            for i, doc in enumerate(st.session_state.eval_rag['documents']):
                with st.expander(f"Documento {i+1} ({len(doc)} caracteres)"):
                    # Show document content
                    st.text_area(
                        f"Contenido del documento {i+1}:",
                        value=doc,
                        height=100,
                        key=f"doc_display_{i}",
                        disabled=True
                    )
                    
                    col_edit, col_delete = st.columns(2)
                    with col_edit:
                        if st.button("✏️ Editar", key=f"edit_{i}"):
                            st.session_state[f'editing_doc_{i}'] = True
                    
                    with col_delete:
                        if st.button("🗑️ Eliminar", key=f"delete_{i}"):
                            st.session_state.eval_rag['documents'].pop(i)
                            # Reset embeddings when documents change
                            st.session_state.eval_rag['embeddings'] = None
                            st.rerun()
                    
                    # Edit mode
                    if st.session_state.get(f'editing_doc_{i}', False):
                        new_content = st.text_area(
                            "Editar contenido:",
                            value=doc,
                            height=150,
                            key=f"edit_content_{i}"
                        )
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.button("💾 Guardar", key=f"save_{i}"):
                                st.session_state.eval_rag['documents'][i] = new_content
                                st.session_state[f'editing_doc_{i}'] = False
                                # Reset embeddings when documents change
                                st.session_state.eval_rag['embeddings'] = None
                                st.success("Documento actualizado")
                                st.rerun()
                        
                        with col_cancel:
                            if st.button("❌ Cancelar", key=f"cancel_{i}"):
                                st.session_state[f'editing_doc_{i}'] = False
                                st.rerun()
        
        with col2:
            st.subheader("➕ Agregar Documento")
            
            new_doc = st.text_area(
                "Contenido del nuevo documento:",
                height=200,
                placeholder="Escribe aquí el contenido del nuevo documento..."
            )
            
            if st.button("📝 Agregar Documento"):
                if new_doc.strip():
                    st.session_state.eval_rag['documents'].append(new_doc.strip())
                    # Reset embeddings when documents change
                    st.session_state.eval_rag['embeddings'] = None
                    st.success("Documento agregado exitosamente")
                    st.rerun()
                else:
                    st.warning("El documento no puede estar vacío")
            
            st.subheader("📊 Estadísticas")
            st.metric("Total documentos", len(st.session_state.eval_rag['documents']))
            
            if st.session_state.eval_rag['documents']:
                avg_length = np.mean([len(doc) for doc in st.session_state.eval_rag['documents']])
                st.metric("Longitud promedio", f"{avg_length:.0f} caracteres")
                
                total_words = sum([len(doc.split()) for doc in st.session_state.eval_rag['documents']])
                st.metric("Total palabras", f"{total_words:,}")
            
            st.subheader("🔄 Acciones")
            
            if st.button("🗑️ Limpiar Todos"):
                if st.session_state.eval_rag['documents']:
                    st.session_state.eval_rag['documents'] = []
                    st.session_state.eval_rag['embeddings'] = None
                    st.success("Todos los documentos eliminados")
                    st.rerun()
            
            # File upload
            uploaded_file = st.file_uploader(
                "📁 Cargar archivo de texto",
                type=['txt', 'md'],
                help="Sube un archivo .txt o .md para agregarlo como documento"
            )
            
            if uploaded_file is not None:
                try:
                    content = uploaded_file.read().decode('utf-8')
                    if st.button("📥 Importar Archivo"):
                        st.session_state.eval_rag['documents'].append(content)
                        st.session_state.eval_rag['embeddings'] = None
                        st.success(f"Archivo '{uploaded_file.name}' importado exitosamente")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error al leer el archivo: {str(e)}")
            
            # Status of embeddings
            st.subheader("🔧 Estado")
            if st.session_state.eval_rag['embeddings'] is not None:
                st.success("✅ Embeddings generados")
            else:
                st.warning("⚠️ Embeddings no generados")
                st.info("Genera embeddings después de modificar documentos")
    
    with tab3:
        st.header("📊 Dashboard de Métricas")
        
        if st.session_state.interaction_logs:
            df = pd.DataFrame([
                {
                    'timestamp': log['timestamp'],
                    'query_length': len(log['query']),
                    'response_length': len(log['response']),
                    **log['metrics']
                }
                for log in st.session_state.interaction_logs
            ])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Tiempo de respuesta")
                fig = px.line(df, x='timestamp', y='total_time', title="Tiempo total por consulta")
                st.plotly_chart(fig, width="stretch")
                
                if 'faithfulness' in df.columns:
                    st.subheader("Distribución de fidelidad")
                    fig = px.histogram(df, x='faithfulness', title="Puntuaciones de fidelidad")
                    st.plotly_chart(fig, width="stretch")
            
            with col2:
                st.subheader("Métricas de recuperación")
                fig = px.scatter(df, x='retrieval_time', y='generation_time', 
                               size='docs_retrieved', title="Recuperación vs generación (tiempo)")
                st.plotly_chart(fig, width="stretch")
                
                if 'relevance' in df.columns and 'context_precision' in df.columns:
                    st.subheader("Calidad vs precisión")
                    fig = px.scatter(df, x='context_precision', y='relevance', 
                                   title="Precisión de contexto vs relevancia")
                    st.plotly_chart(fig, width="stretch")
            
            st.subheader("📈 Estadísticas generales")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Consultas totales", len(df))
            with col2:
                st.metric("Tiempo promedio", f"{df['total_time'].mean():.2f}s")
            with col3:
                if 'faithfulness' in df.columns:
                    st.metric("Fidelidad promedio", f"{df['faithfulness'].mean():.1f}/10")
            with col4:
                if 'relevance' in df.columns:
                    st.metric("Relevancia promedio", f"{df['relevance'].mean():.1f}/10")
        else:
            st.info("No hay datos de interacciones aún. Realiza algunas consultas primero.")
    
    with tab4:
        st.header("🧪 Evaluación Sistemática")
        st.info(
            "Cada caso ejecuta recuperación, generación y **varias** llamadas de evaluación. "
            "Usa la **barra de progreso** y el texto bajo el botón; el proceso es lento pero normal."
        )
        
        if st.button("🧪 Ejecutar Evaluación Completa"):
            logger.info("UI: clic Evaluación completa")
            if st.session_state.eval_rag['embeddings'] is None:
                st.warning("Genera embeddings primero")
            elif st.session_state.eval_rag['embeddings_model'] is None:
                st.warning("Modelo de embeddings no inicializado")
            else:
                eval_dataset = create_evaluation_dataset()
                results = []
                n_cases = len(eval_dataset)
                prog = st.progress(0.0)
                step_label = st.empty()
                
                for ci, test_case in enumerate(eval_dataset):
                    query = test_case['query']
                    logger.info("EVAL sistema caso %d/%d: %s", ci + 1, n_cases, query[:80])
                    step_label.markdown(
                        f"**Paso {ci + 1}/{n_cases}** — `{query[:70]}{'…' if len(query) > 70 else ''}` — **recuperando**…"
                    )
                    prog.progress(min(1.0, (ci + 0.2) / n_cases))
                    
                    docs, retrieval_time = hybrid_search_with_metrics(
                        query,
                        st.session_state.eval_rag['documents'],
                        st.session_state.eval_rag['embeddings'],
                        st.session_state.eval_rag['embeddings_model'],
                        3,
                    )
                    
                    if docs:
                        step_label.markdown(
                            f"**Paso {ci + 1}/{n_cases}** — **generando respuesta** (puede tardar)…"
                        )
                        prog.progress(min(1.0, (ci + 0.45) / n_cases))
                        response, generation_time = generate_response_with_metrics(client, query, docs)
                        
                        context_text = "".join([d['document'] for d in docs])
                        step_label.markdown(
                            f"**Paso {ci + 1}/{n_cases}** — **métricas LLM** "
                            f"(fidelidad + relevancia + {len(docs)}× precisión contexto)…"
                        )
                        prog.progress(min(1.0, (ci + 0.7) / n_cases))
                        faithfulness = evaluate_faithfulness(client, query, context_text, response)
                        relevance = evaluate_relevance(client, query, response)
                        context_precision = evaluate_context_precision(client, query, docs)
                        
                        results.append({
                            'query': query,
                            'response': response,
                            'retrieval_time': retrieval_time,
                            'generation_time': generation_time,
                            'faithfulness': faithfulness,
                            'relevance': relevance,
                            'context_precision': context_precision,
                            'ground_truth': test_case['ground_truth']
                        })
                    prog.progress(min(1.0, (ci + 1) / n_cases))
                
                step_label.markdown("**Evaluación sistemática terminada.**")
                prog.progress(1.0)
                logger.info("EVAL sistema: %d casos con resultado", len(results))
                
                if results:
                    st.subheader("📊 Resultados de Evaluación")
                    eval_df = pd.DataFrame(results)
                    st.dataframe(eval_df)
                    st.toast(f"Evaluación lista: {len(results)} casos.", icon="✅")
                    
                    st.subheader("📈 Métricas Promedio")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Fidelidad", f"{eval_df['faithfulness'].mean():.1f}/10")
                    with col2:
                        st.metric("Relevancia", f"{eval_df['relevance'].mean():.1f}/10")
                    with col3:
                        st.metric("Precisión", f"{eval_df['context_precision'].mean():.2f}")
                    with col4:
                        st.metric("Tiempo total", f"{(eval_df['retrieval_time'] + eval_df['generation_time']).mean():.2f}s")
                else:
                    st.error("No se pudieron obtener resultados de evaluación")
    
    with tab5:
        st.header("📈 Analytics y Exportación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Exportar Datos")
            
            if st.button("📊 Exportar para LangSmith"):
                logger.info("UI: Exportar LangSmith (vista previa)")
                if st.session_state.interaction_logs:
                    langsmith_data = export_langsmith_format(st.session_state.interaction_logs)
                    st.json(langsmith_data[:2])
                    
                    json_str = json.dumps(langsmith_data, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="💾 Descargar JSON LangSmith",
                        data=json_str,
                        file_name=f"langsmith_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.info("No hay datos para exportar")
            
            if st.button("📊 Exportar CSV"):
                logger.info("UI: Exportar CSV preparado")
                if st.session_state.interaction_logs:
                    df = pd.DataFrame([
                        {
                            'timestamp': log['timestamp'],
                            'query': log['query'],
                            'response': _truncate_for_csv(log['response']),
                            **log['metrics']
                        }
                        for log in st.session_state.interaction_logs
                    ])
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="💾 Descargar CSV",
                        data=csv,
                        file_name=f"rag_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                    )
                else:
                    st.info("No hay datos para exportar")
        
        with col2:
            st.subheader("📊 Vista del corpus")
            
            if st.session_state.eval_rag['documents']:
                # Document statistics
                doc_lengths = [len(doc) for doc in st.session_state.eval_rag['documents']]
                
                fig = px.bar(
                    x=list(range(1, len(doc_lengths) + 1)),
                    y=doc_lengths,
                    title="Longitud de documentos",
                    labels={'x': 'Documento #', 'y': 'Caracteres'}
                )
                st.plotly_chart(fig, width="stretch")
                
                # Word frequency analysis
                all_text = " ".join(st.session_state.eval_rag['documents'])
                words = re.findall(r"\w+", all_text.lower())
                word_freq = {}
                for word in words:
                    if len(word) > 1:
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
                
                if top_words:
                    fig = px.bar(
                        x=[word[0] for word in top_words],
                        y=[word[1] for word in top_words],
                        title="10 palabras más frecuentes",
                    )
                    st.plotly_chart(fig, width="stretch")
            else:
                st.info("No hay documentos para analizar.")

if __name__ == "__main__":
    main()
