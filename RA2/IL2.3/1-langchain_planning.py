"""
IL2.3: Planificación con LangChain
=================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos usando herramientas.
"""

# Requiere: pip install langchain langchain-classic langchain-groq groq python-dotenv
# (langchain-classic es obligatorio: create_react_agent / AgentExecutor / hub viven ahi en LangChain 1.x)
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.agents import create_react_agent, AgentExecutor, Tool

import ast
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv no está instalado. Instálalo con: pip install python-dotenv")
    exit(1)

# Obtener variables de entorno
if not os.getenv("GROQ_API_KEY"):
    print("❌ GROQ_API_KEY no está configurada. Por favor verifica tu archivo .env")
    print("💡 Tu archivo .env debe contener: GROQ_API_KEY=gsk_tu_clave_aqui")
    exit(1)

# Herramienta personalizada: suma
def sumar(x):
    try:
        # Evaluacion acotada: AST + eval del arbol compilado con builtins restringidos
        # (solo demostracion; en produccion preferir un parser numerico dedicado).
        tree = ast.parse(x, mode="eval")
        result = eval(compile(tree, "<string>", "eval"), {"__builtins__": {}})
        return str(result)
    except Exception:
        return "Error en la operación"

herramienta_suma = Tool(
    name="Calculadora",
    func=sumar,
    description="Realiza sumas y operaciones matemáticas simples."
)

# Inicializa el LLM y el agente (ChatGroq lee GROQ_API_KEY del entorno automáticamente)
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    temperature=0,
    reasoning_effort="low",
)

print("✅ LLM configurado correctamente")

# El prompt ReAct, definido aquí en vez de descargarlo del hub de LangChain.
# Antes era `hub.pull("hwchase17/react")`: necesitaba red y deserializaba un objeto
# de un tercero. Tenerlo a la vista es además mejor para entender cómo razona el agente.
PLANTILLA_REACT = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(PLANTILLA_REACT)
agent = create_react_agent(llm, tools=[herramienta_suma], prompt=prompt)
agente = AgentExecutor(agent=agent, tools=[herramienta_suma], verbose=True)

if __name__ == "__main__":
    print("Planificación y ejecución con LangChain:")
    resultado = agente.invoke({"input": "¿Cuánto es 55 + 1020 ?"})["output"]
    print(resultado)