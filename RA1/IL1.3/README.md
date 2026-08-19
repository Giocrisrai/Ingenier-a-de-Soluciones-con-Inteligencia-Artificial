# RA1 - IL1.3: Infraestructura RAG (Retrieval-Augmented Generation)

En este módulo de aprendizaje, exploraremos la arquitectura de **Recuperación Aumentada por Generación (RAG)**, una técnica poderosa para conectar Modelos de Lenguaje Grandes (LLMs) con fuentes de conocimiento externas y actualizadas.

## ¿Qué es RAG?

RAG es un enfoque que mejora las respuestas de los LLMs al permitirles consultar una base de conocimiento externa antes de generar una respuesta. Esto reduce las "alucinaciones" y asegura que la información proporcionada sea relevante y precisa.

## Contenido del Módulo

Este módulo se divide en los siguientes cuadernos de Jupyter, diseñados para guiarte progresivamente a través de los conceptos de RAG:

1.  **`1-basic-rag.ipynb`**: Introduce los conceptos fundamentales de RAG con un ejemplo simple y práctico.
2.  **`2-text-chunking.py`**: Explora diferentes estrategias para dividir texto en fragmentos (chunks), un paso crucial para la eficiencia del recuperador. **No es un notebook, sino una app de Streamlit**: se lanza desde la terminal con `streamlit run RA1/IL1.3/2-text-chunking.py` (no necesita API key: solo divide texto).
3.  **`3-embeddings-simple-rag.ipynb`**: Muestra cómo generar embeddings a partir de fragmentos de texto y cómo utilizarlos para construir un sistema RAG básico.
4.  **`4-vector-rag.ipynb`**: Avanza hacia una implementación más robusta utilizando una base de datos vectorial para almacenar y consultar eficientemente los embeddings.

## Objetivos de Aprendizaje

Al finalizar este módulo, serás capaz de:

-   Comprender la arquitectura y los componentes de un sistema RAG.
-   Implementar un flujo RAG básico para responder preguntas basadas en un documento.
-   Aplicar técnicas de text chunking para procesar documentos.
-   Utilizar modelos de embeddings para convertir texto en representaciones vectoriales.
-   Integrar una base de datos vectorial para crear un sistema RAG escalable.

## Arquitectura del RAG en este módulo: dos proveedores, no uno

Un detalle importante que verás en todos los notebooks: **la generación y los embeddings no vienen del mismo sitio**.

| Pieza del RAG | Dónde se ejecuta | Modelo | Coste |
|---|---|---|---|
| Generación (chat) | API de **Groq** | `openai/gpt-oss-120b` | API key gratuita |
| Embeddings | **Tu propia máquina** (HuggingFace / sentence-transformers) | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | gratis, sin API key |

¿Por qué? Porque **Groq no ofrece un endpoint de embeddings**: su API solo expone chat/completions. Al construir un RAG sobre Groq hay que resolver los vectores por otra vía, y la más simple es calcularlos localmente con `langchain-huggingface`.

Lejos de ser un parche, esta separación es una práctica habitual en producción:

-   **Coste cero por token**: embedar un corpus grande con una API de pago es caro; en local es solo tiempo de CPU.
-   **Privacidad**: tus documentos no salen de la máquina.
-   **Funciona sin conexión** una vez descargado el modelo.

A cambio, dos cosas que conviene saber antes de ejecutar:

-   La **primera ejecución descarga ~470 MB** del modelo desde HuggingFace (después queda en caché y arranca en segundos).
-   Los vectores tienen **384 dimensiones** en vez de las 1536 típicas de los modelos comerciales: menos memoria y búsquedas más rápidas, a cambio de algo de precisión semántica.

La interfaz de LangChain es idéntica en ambos casos (`embed_documents`, `embed_query`), así que FAISS y el resto del pipeline funcionan sin cambios.

## Instrucciones

Para comenzar, abre y ejecuta los cuadernos en el orden listado (el paso 2 se lanza desde la terminal con `streamlit run`, no desde Jupyter). Asegúrate de tener las variables de entorno (`GROQ_API_KEY`, `GROQ_MODEL`, `EMBEDDING_MODEL`) configuradas como se describe en el `README.md` principal del repositorio. Puedes crear tu API key gratuita en [console.groq.com](https://console.groq.com/).