#!/usr/bin/env python3
"""Comprueba que la configuración de Groq del curso funciona de verdad.

Uso:  uv run python scripts/verify_groq.py

Hace cuatro comprobaciones, de más barata a más cara:
  1. Que GROQ_API_KEY esté definida y tenga pinta de key válida.
  2. Que el SDK oficial (`groq`) pueda llamar al modelo.
  3. Que `ChatGroq` de LangChain pueda llamar al modelo.
  4. Que los embeddings locales de HuggingFace funcionen (sin API key).

Gasta muy pocos tokens: pide respuestas de una palabra.
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

load_dotenv()

MODELO = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
MODELO_RAPIDO = os.getenv("GROQ_MODEL_FAST", "openai/gpt-oss-20b")
MODELO_EMBEDDINGS = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

PREGUNTA = "Responde solo con la palabra: OK"


def _fallo(mensaje: str) -> None:
    print(f"ERROR  {mensaje}", file=sys.stderr)
    sys.exit(1)


def comprobar_api_key() -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        _fallo(
            "Falta GROQ_API_KEY.\n"
            "       Local: copia .env.example a .env y pega tu key.\n"
            "       Colab: guárdala en Secrets con el nombre GROQ_API_KEY.\n"
            "       Obtenla en https://console.groq.com/ > API Keys > Create API Key"
        )
    if not api_key.startswith("gsk_"):
        print("AVISO  La key no empieza por 'gsk_'; revisa que la copiaste completa.")
    # NUNCA imprimimos caracteres de la key, ni siquiera "solo el principio y el final":
    # ese fragmento ya es parte del secreto. Confirmamos formato y longitud, nada más.
    print("OK     API Key configurada:", "✓" if api_key.startswith("gsk_") else "✗ revisa tu key")
    print(f"OK     Longitud de la key: {len(api_key)} caracteres")
    return api_key


def comprobar_sdk() -> None:
    from groq import Groq

    cliente = Groq()
    respuesta = cliente.chat.completions.create(
        model=MODELO_RAPIDO,
        messages=[{"role": "user", "content": PREGUNTA}],
        max_tokens=16,
        temperature=0,
        reasoning_effort="low",
    )
    contenido = (respuesta.choices[0].message.content or "").strip()
    print(f"OK     SDK groq · modelo {MODELO_RAPIDO} · respuesta: {contenido!r}")


def comprobar_langchain() -> None:
    from langchain_groq import ChatGroq

    llm = ChatGroq(model=MODELO, temperature=0, max_tokens=16, reasoning_effort="low")
    contenido = (llm.invoke(PREGUNTA).content or "").strip()
    print(f"OK     ChatGroq   · modelo {MODELO} · respuesta: {contenido!r}")


def comprobar_embeddings() -> None:
    print(f"...    Cargando embeddings locales ({MODELO_EMBEDDINGS}).")
    print("       La primera vez descarga ~470 MB; después queda en caché.")
    from langchain_huggingface import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name=MODELO_EMBEDDINGS,
        encode_kwargs={"normalize_embeddings": True},
    )
    vectores = embeddings.embed_documents(["hola mundo", "el gato duerme"])
    print(f"OK     Embeddings · {len(vectores)} vectores de {len(vectores[0])} dimensiones (sin API key)")


def main() -> None:
    print("Verificando la configuración de Groq del curso…\n")
    comprobar_api_key()
    try:
        comprobar_sdk()
        comprobar_langchain()
    except Exception as e:  # noqa: BLE001 — queremos un mensaje legible para el alumno
        nombre = type(e).__name__
        if "AuthenticationError" in nombre:
            _fallo(f"La API key fue rechazada por Groq ({nombre}). Genera una nueva en console.groq.com.")
        if "RateLimitError" in nombre:
            _fallo(
                f"Alcanzaste el límite de la capa gratuita ({nombre}).\n"
                "       Lee el mensaje del error: dice si fue por minuto (TPM, espera y reintenta)\n"
                "       o por día (TPD: 200K en gpt-oss-120b y gpt-oss-20b)."
            )
        _fallo(f"Fallo al llamar a Groq ({nombre}): {e}")
    comprobar_embeddings()
    print("\nListo: Groq y los embeddings locales funcionan correctamente.")


if __name__ == "__main__":
    main()
