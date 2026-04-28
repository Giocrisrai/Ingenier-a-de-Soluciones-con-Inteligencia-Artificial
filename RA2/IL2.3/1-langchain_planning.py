"""
IL2.3: Planificación con LangChain
=================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos usando herramientas.
"""

# Requiere: pip install langchain langchain-openai openai python-dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor, Tool
from langchain_classic import hub
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
github_token = os.getenv("GITHUB_TOKEN")
github_base_url = os.getenv("GITHUB_BASE_URL", "https://models.inference.ai.azure.com")

if not github_token:
    print("❌ GITHUB_TOKEN no está configurado. Por favor verifica tu archivo .env")
    print("💡 Tu archivo .env debe contener: GITHUB_TOKEN=tu_token_aqui")
    exit(1)

# Herramienta personalizada: suma
def sumar(x):
    try:
        # Evaluar expresion matematica de forma segura
        tree = ast.parse(x, mode='eval')
        result = eval(compile(tree, '<string>', 'eval'), {"__builtins__": {}})
        return str(result)
    except Exception:
        return "Error en la operación"

herramienta_suma = Tool(
    name="Calculadora",
    func=sumar,
    description="Realiza sumas y operaciones matemáticas simples."
)

# Inicializa el LLM y el agente
llm = ChatOpenAI(
    model="gpt-4o",
    base_url=github_base_url,
    api_key=github_token,
    temperature=0
)

print("✅ LLM configurado correctamente")

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools=[herramienta_suma], prompt=prompt)
agente = AgentExecutor(agent=agent, tools=[herramienta_suma], verbose=True)

if __name__ == "__main__":
    print("Planificación y ejecución con LangChain:")
    resultado = agente.invoke({"input": "¿Cuánto es 55 X 100?"})["output"]
    print(resultado)