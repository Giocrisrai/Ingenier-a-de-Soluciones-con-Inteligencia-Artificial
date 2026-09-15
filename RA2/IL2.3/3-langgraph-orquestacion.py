"""
IL2.3: Orquestación con grafo agentico (LangGraph)
=================================================
Compara tres formas de coordinar trabajo:

1. Python puro (2-multiagent_orchestration.py, 6-workflow-management.py)
   → algoritmos y DAGs, sin LLM
2. CrewAI (2-crewai_orchestration.py)
   → roles, tasks y process.sequential
3. Este archivo
   → un grafo explícito: clasificar → especialista → sintetizar

El punto didáctico: un "equipo" no exige CrewAI. A veces es un grafo
con nodos y una arista condicional. El criterio es: ¿los roles son
prompts incompatibles, o solo pasos de una función?
"""

from __future__ import annotations

import os
from typing import Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("❌ GROQ_API_KEY no está configurada. Verifica tu archivo .env")
    raise SystemExit(1)

# Modelo rápido: este script hace 3 llamadas cortas por consulta.
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL_FAST", "openai/gpt-oss-20b"),
    temperature=0,
    reasoning_effort="low",
)


class EstadoEquipo(TypedDict):
    consulta: str
    destino: str
    borrador: str
    respuesta: str


def clasificar(state: EstadoEquipo) -> dict:
    """El supervisor solo elige la ruta. No resuelve la tarea."""
    decision = llm.invoke(
        [
            SystemMessage(
                content=(
                    "Clasifica la consulta en UNA palabra: "
                    "tecnico, comercial o general. Sin explicación."
                )
            ),
            HumanMessage(content=state["consulta"]),
        ]
    )
    destino = (decision.content or "general").strip().lower()
    if destino not in {"tecnico", "comercial", "general"}:
        destino = "general"
    print(f"🧭 Supervisor → ruta '{destino}'")
    return {"destino": destino}


def experto_tecnico(state: EstadoEquipo) -> dict:
    texto = llm.invoke(
        [
            SystemMessage(content="Eres un experto técnico. Responde en 4-6 líneas."),
            HumanMessage(content=state["consulta"]),
        ]
    ).content
    return {"borrador": texto}


def experto_comercial(state: EstadoEquipo) -> dict:
    texto = llm.invoke(
        [
            SystemMessage(
                content="Eres un experto comercial. Responde en 4-6 líneas, con beneficio y riesgo."
            ),
            HumanMessage(content=state["consulta"]),
        ]
    ).content
    return {"borrador": texto}


def experto_general(state: EstadoEquipo) -> dict:
    texto = llm.invoke(
        [
            SystemMessage(content="Eres un asistente general. Responde en 4-6 líneas."),
            HumanMessage(content=state["consulta"]),
        ]
    ).content
    return {"borrador": texto}


def sintetizar(state: EstadoEquipo) -> dict:
    texto = llm.invoke(
        [
            SystemMessage(
                content=(
                    "Redacta la respuesta final para el usuario a partir del borrador. "
                    "No menciones que hay un equipo ni un supervisor."
                )
            ),
            HumanMessage(content=state["borrador"]),
        ]
    ).content
    return {"respuesta": texto}


def enrutar(state: EstadoEquipo) -> Literal["tecnico", "comercial", "general"]:
    return state["destino"]  # type: ignore[return-value]


grafo = StateGraph(EstadoEquipo)
grafo.add_node("clasificar", clasificar)
grafo.add_node("tecnico", experto_tecnico)
grafo.add_node("comercial", experto_comercial)
grafo.add_node("general", experto_general)
grafo.add_node("sintetizar", sintetizar)
grafo.add_edge(START, "clasificar")
grafo.add_conditional_edges(
    "clasificar",
    enrutar,
    {"tecnico": "tecnico", "comercial": "comercial", "general": "general"},
)
grafo.add_edge("tecnico", "sintetizar")
grafo.add_edge("comercial", "sintetizar")
grafo.add_edge("general", "sintetizar")
grafo.add_edge("sintetizar", END)
equipo = grafo.compile()


def mostrar_grafo(app) -> None:
    """draw_ascii pide grandalf; este listado no añade dependencias."""
    g = app.get_graph()
    print("Nodos:", ", ".join(n.name for n in g.nodes.values()))
    for e in g.edges:
        marca = "  (condicional)" if getattr(e, "conditional", False) else ""
        print(f"  {e.source} → {e.target}{marca}")


if __name__ == "__main__":
    print("✅ Grafo agentico listo (supervisor + especialistas)\n")
    mostrar_grafo(equipo)
    consultas = [
        "¿Qué latencia tiene Groq frente a un GPU local para un LLM de 20B?",
        "¿Conviene vender un chatbot a un colegio si el presupuesto es bajo?",
    ]
    for consulta in consultas:
        print(f"\n=== {consulta} ===")
        salida = equipo.invoke(
            {"consulta": consulta, "destino": "", "borrador": "", "respuesta": ""}
        )
        print(salida["respuesta"])
