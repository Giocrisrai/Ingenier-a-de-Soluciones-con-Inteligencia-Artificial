"""
IL2.3: Orquestación Multi-Agente con CrewAI
==========================================
Ejemplo de cómo dos agentes CrewAI colaboran para resolver una tarea.
"""

# Requiere: pip install "crewai[litellm]" crewai-tools python-dotenv
# (el extra [litellm] es obligatorio: sin el, LLM(model="groq/...") falla con ImportError)
from crewai import Agent, Task, Crew, LLM
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

# LLM de CrewAI apuntando a Groq (el prefijo "groq/" es obligatorio: CrewAI usa LiteLLM)
llm = LLM(
    model=f"groq/{os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}",
    temperature=0.2,
)

print("✅ LLM de Groq configurado para CrewAI")

# Agente 1: Investigador
investigador = Agent(
    role="Investigador",
    goal="Buscar información sobre la capital de Francia",
    backstory="Eres experto en encontrar datos rápidos.",
    llm=llm
)

# Agente 2: Redactor
redactor = Agent(
    role="Redactor",
    goal="Redactar una respuesta clara y breve",
    backstory="Eres especialista en explicar conceptos de forma sencilla.",
    llm=llm
)

# Tareas
tarea_investigar = Task(
    description="Busca cuál es la capital de Francia",
    expected_output="El nombre de la capital de Francia",
    agent=investigador
)
tarea_redactar = Task(
    description="Redacta una respuesta usando la información encontrada",
    expected_output="Una respuesta clara y breve sobre la capital de Francia",
    agent=redactor,
    context=[tarea_investigar]
)

# Crew (equipo)
crew = Crew(
    agents=[investigador, redactor],
    tasks=[tarea_investigar, tarea_redactar],
    verbose=True
)

if __name__ == "__main__":
    print("Orquestación multi-agente con CrewAI:")
    print(crew.kickoff()) 