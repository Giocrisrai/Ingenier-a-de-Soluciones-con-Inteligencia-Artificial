"""
IL2.3: Planificación con LangGraph (camino actual)
=================================================
El mismo problema que 1-basic_planning.py y 1-langchain_planning.py,
pero con el runtime vigente: `create_agent` (LangChain 1.x sobre LangGraph).

Compara con:
- 1-basic_planning.py / 1-langchain_planning.py → AgentExecutor + ReAct por prompt
  (modo clásico; sigue siendo útil para leer código viejo)
- Este archivo → grafo de agente con tool calling nativo
"""

from __future__ import annotations

import ast
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("❌ GROQ_API_KEY no está configurada. Verifica tu archivo .env")
    raise SystemExit(1)

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    temperature=0,
    reasoning_effort="low",
)


@tool
def pasos_cafe(_consulta: str = "") -> str:
    """Devuelve los pasos para preparar café."""
    return (
        "1. Calentar agua\n"
        "2. Añadir café al filtro\n"
        "3. Verter agua caliente\n"
        "4. Servir en una taza"
    )


@tool
def calculadora(expresion: str) -> str:
    """Evalúa una operación matemática simple, por ejemplo '55 + 1020'."""
    try:
        # Demo didáctica: AST + eval sin builtins. En producción usa un parser numérico.
        arbol = ast.parse(expresion, mode="eval")
        resultado = eval(compile(arbol, "<string>", "eval"), {"__builtins__": {}})
        return str(resultado)
    except Exception:
        return "Error en la operación"


agente = create_agent(
    model=llm,
    tools=[pasos_cafe, calculadora],
    system_prompt=(
        "Eres un asistente que usa herramientas cuando necesita un procedimiento "
        "o un cálculo. No inventes números: usa la calculadora."
    ),
)


def preguntar(texto: str) -> str:
    salida = agente.invoke({"messages": [{"role": "user", "content": texto}]})
    return salida["messages"][-1].content


def mostrar_grafo(app) -> None:
    """draw_ascii pide grandalf; este listado no añade dependencias."""
    g = app.get_graph()
    print("Nodos:", ", ".join(n.name for n in g.nodes.values()))
    for e in g.edges:
        marca = "  (condicional)" if getattr(e, "conditional", False) else ""
        print(f"  {e.source} → {e.target}{marca}")


if __name__ == "__main__":
    print("✅ Agente LangGraph listo (create_agent)\n")
    print("Grafo del agente:")
    mostrar_grafo(agente)
    print("\n--- Consulta 1 ---")
    print(preguntar("¿Cuáles son los pasos para preparar café?"))
    print("\n--- Consulta 2 ---")
    print(preguntar("¿Cuánto es 55 + 1020?"))
