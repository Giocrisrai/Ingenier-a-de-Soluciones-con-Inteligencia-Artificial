"""
IL3.1: Observar un grafo LangGraph (opcional, 1-2 llamadas Groq)
================================================================
El notebook de este modulo usa el SDK crudo a proposito (ves tokens y
latencia de UNA llamada). Este script aplica las mismas metricas al
runtime de RA2: create_agent + InMemorySaver + thread_id.

Ejecutar: uv run python RA3/IL3.1/3-observar-grafo.py
"""

from __future__ import annotations

import ast
import os
import time
import uuid

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("GROQ_API_KEY no esta configurada. Verifica tu archivo .env")
    raise SystemExit(1)


@tool
def calculadora(expresion: str) -> str:
    """Evalua una expresion aritmetica simple (+ - * /)."""
    arbol = ast.parse(expresion.strip(), mode="eval")
    permitidos = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                  ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd)
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, permitidos):
            return f"Operacion no permitida: {type(nodo).__name__}"
    return str(eval(compile(arbol, "<calc>", "eval")))


modelo = os.getenv("GROQ_MODEL_FAST", "openai/gpt-oss-20b")
llm = ChatGroq(model=modelo, temperature=0, reasoning_effort="low")
agente = create_agent(model=llm, tools=[calculadora], checkpointer=InMemorySaver())

thread_id = f"obs-{uuid.uuid4().hex[:8]}"
consulta = "Cuanto es 55 + 1020? Usa la calculadora."

print(f"Modelo: {modelo}")
print(f"thread_id: {thread_id}  (es el identificador de conversacion de IL2.2)")
print(f"Consulta: {consulta}\n")

inicio = time.perf_counter()
resultado = agente.invoke(
    {"messages": [{"role": "user", "content": consulta}]},
    config={"configurable": {"thread_id": thread_id}},
)
duracion_ms = (time.perf_counter() - inicio) * 1000

mensajes = resultado["messages"]
roles = [type(m).__name__ for m in mensajes]
herramientas = [
    getattr(m, "name", None)
    for m in mensajes
    if type(m).__name__ == "ToolMessage"
]
final = mensajes[-1].content if mensajes else ""

print(f"Duracion total: {duracion_ms:.0f} ms")
print(f"Mensajes en el hilo: {len(mensajes)} → {roles}")
print(f"Tools disparadas: {herramientas or '(ninguna)'}")
print(f"Respuesta: {final[:400]}")
print()
print("Que anotar en el ADR (IL2.4) / LangSmith (IL3.2):")
print("  - thread_id de la sesion")
print("  - cuantos mensajes (cada tool call es un span)")
print("  - ms de punta a punta, no solo de una llamada al LLM")
