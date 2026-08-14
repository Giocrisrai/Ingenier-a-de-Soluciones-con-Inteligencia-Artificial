"""
IL2.3: Planificación Básica con LangChain
========================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos simples usando una herramienta.
"""

# Requiere: pip install langchain langchain-classic langchain-groq groq python-dotenv
# (langchain-classic es obligatorio: create_react_agent / AgentExecutor / hub viven ahi en LangChain 1.x)
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.agents import create_react_agent, AgentExecutor, Tool

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

# Configurar el LLM (ChatGroq lee GROQ_API_KEY del entorno automáticamente)
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    temperature=0
)

print("✅ LLM configurado correctamente")

# Herramienta personalizada: pasos para preparar café
def pasos_cafe(_):
    return "1. Calentar agua\n2. Añadir café al filtro\n3. Verter agua caliente\n4. Servir en una taza"

herramienta_cafe = Tool(
    name="PasosCafé",
    func=pasos_cafe,
    description="Devuelve los pasos para preparar café."
)

# Inicializa el agente
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
agent = create_react_agent(llm, tools=[herramienta_cafe], prompt=prompt)
agente = AgentExecutor(agent=agent, tools=[herramienta_cafe], verbose=True)

if __name__ == "__main__":
    print("Planificación con LangChain:")
    print(agente.invoke({"input": "¿Cuáles son los pasos para preparar café?"})["output"])