"""
IL2.3: Planificación Básica con LangChain
========================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos simples usando una herramienta.
"""

# Requiere: pip install langchain langchain-classic langchain-groq groq python-dotenv
# (langchain-classic es obligatorio: create_react_agent / AgentExecutor / hub viven ahi en LangChain 1.x)
from langchain_groq import ChatGroq
from langchain_classic.agents import create_react_agent, AgentExecutor, Tool
from langchain_classic import hub
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
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools=[herramienta_cafe], prompt=prompt)
agente = AgentExecutor(agent=agent, tools=[herramienta_cafe], verbose=True)

if __name__ == "__main__":
    print("Planificación con LangChain:")
    print(agente.invoke({"input": "¿Cuáles son los pasos para preparar café?"})["output"])