"""
IL2.3: Orquestación de Agentes con LangChain
==========================================

Este módulo demuestra cómo orquestar múltiples agentes especializados que
trabajan juntos para resolver problemas complejos.

Conceptos Clave:
- Especialización de agentes por dominio
- Coordinación y comunicación entre agentes
- Delegación de tareas según capacidades
- Integración de resultados de múltiples agentes

Para Estudiantes:
La orquestación de agentes permite dividir problemas complejos entre varios
expertos, cada uno enfocado en su área. Por ejemplo, en una empresa: un agente
para ventas, otro para soporte técnico, otro para análisis de datos.
"""

# Requiere: pip install langchain langchain-openai openai python-dotenv
from langchain_openai import ChatOpenAI
from typing import Dict, List, Any
import os
import json

from _demo_utils import pause_demo

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

# Configurar LLM
llm = ChatOpenAI(
    model="gpt-4o",
    base_url=github_base_url,
    api_key=github_token,
    temperature=0.7
)

print("✅ LLM configurado correctamente\n")


class SpecializedAgent:
    """
    Agente especializado en un dominio específico
    
    Atributos:
        name: Nombre del agente
        specialty: Área de especialización
        llm: Modelo de lenguaje
        capabilities: Lista de capacidades
    """
    
    def __init__(self, name: str, specialty: str, capabilities: List[str]):
        self.name = name
        self.specialty = specialty
        self.capabilities = capabilities
        self.llm = llm
        self.tasks_completed = 0
        
        print(f"🤖 Agente '{name}' creado")
        print(f"   Especialidad: {specialty}")
        print(f"   Capacidades: {', '.join(capabilities)}")
    
    def can_handle(self, task_type: str) -> bool:
        """Verifica si el agente puede manejar un tipo de tarea"""
        return task_type.lower() in [c.lower() for c in self.capabilities]
    
    def execute_task(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Ejecuta una tarea usando su especialización
        
        Args:
            task: Descripción de la tarea
            context: Contexto adicional
            
        Returns:
            Diccionario con el resultado
        """
        print(f"\n🔧 {self.name} trabajando en: '{task}'")
        
        # Prompt especializado
        prompt = f"""
        Eres un agente especializado en {self.specialty}.
        Tus capacidades son: {', '.join(self.capabilities)}.
        
        Tarea: {task}
        {f"Contexto: {context}" if context else ""}
        
        Proporciona una respuesta detallada y profesional basada en tu especialización.
        """
        
        try:
            response = self.llm.invoke(prompt)
            self.tasks_completed += 1
            
            result = {
                "agent": self.name,
                "specialty": self.specialty,
                "task": task,
                "result": response.content,
                "status": "completed"
            }
            
            print(f"   ✅ Tarea completada por {self.name}")
            return result
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {
                "agent": self.name,
                "task": task,
                "result": None,
                "status": "failed",
                "error": str(e)
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del agente"""
        return {
            "name": self.name,
            "specialty": self.specialty,
            "tasks_completed": self.tasks_completed
        }


class Orchestrator:
    """
    Orquestador que coordina múltiples agentes
    
    Atributos:
        agents: Lista de agentes especializados
        task_history: Historial de tareas ejecutadas
    """
    
    def __init__(self, name: str = "Orquestador Principal"):
        self.name = name
        self.agents: List[SpecializedAgent] = []
        self.task_history: List[Dict[str, Any]] = []
        
        print(f"\n🎭 {name} inicializado")
    
    def register_agent(self, agent: SpecializedAgent):
        """Registra un nuevo agente en el sistema"""
        self.agents.append(agent)
        print(f"   ✅ Agente '{agent.name}' registrado")
    
    def find_suitable_agent(self, task_type: str) -> SpecializedAgent:
        """
        Encuentra el agente más adecuado para una tarea
        
        Args:
            task_type: Tipo de tarea
            
        Returns:
            Agente especializado o None
        """
        for agent in self.agents:
            if agent.can_handle(task_type):
                return agent
        return None
    
    def delegate_task(self, task_type: str, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Delega una tarea al agente más apropiado
        
        Args:
            task_type: Tipo de tarea
            task_description: Descripción de la tarea
            context: Contexto adicional
            
        Returns:
            Resultado de la ejecución
        """
        print(f"\n📋 Delegando tarea de tipo: {task_type}")
        
        # Encontrar agente apropiado
        agent = self.find_suitable_agent(task_type)
        
        if agent is None:
            print(f"   ⚠️ No hay agente disponible para '{task_type}'")
            return {
                "status": "no_agent",
                "task_type": task_type,
                "task": task_description
            }
        
        print(f"   ➡️  Asignado a: {agent.name}")
        
        # Ejecutar tarea
        result = agent.execute_task(task_description, context)
        
        # Guardar en historial
        self.task_history.append(result)
        
        return result
    
    def execute_workflow(self, workflow: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ejecuta un flujo de trabajo completo
        
        Args:
            workflow: Lista de tareas con su tipo y descripción
            
        Returns:
            Lista de resultados
        """
        print(f"\n\n🚀 Ejecutando workflow con {len(workflow)} tareas")
        print("=" * 70)
        
        results = []
        context = {}
        
        for i, task in enumerate(workflow, 1):
            print(f"\n--- Tarea {i}/{len(workflow)} ---")
            
            result = self.delegate_task(
                task_type=task["type"],
                task_description=task["description"],
                context=context
            )
            
            results.append(result)
            
            # Actualizar contexto con resultados previos
            if result["status"] == "completed":
                context[f"task_{i}_result"] = result["result"]
        
        return results
    
    def generate_report(self):
        """Genera un reporte de actividad"""
        print(f"\n\n📊 REPORTE DE ORQUESTACIÓN")
        print("=" * 70)
        
        print(f"\nAgentes activos: {len(self.agents)}")
        for agent in self.agents:
            stats = agent.get_stats()
            print(f"   • {stats['name']}: {stats['tasks_completed']} tareas completadas")
        
        print(f"\nTotal de tareas en historial: {len(self.task_history)}")
        
        completed = sum(1 for t in self.task_history if t["status"] == "completed")
        failed = sum(1 for t in self.task_history if t["status"] == "failed")
        
        print(f"   ✅ Completadas: {completed}")
        print(f"   ❌ Fallidas: {failed}")


def demo_software_development_team():
    """
    Demostración: Equipo de Desarrollo de Software
    """
    print("="*70)
    print("  🎓 DEMOSTRACIÓN: EQUIPO DE DESARROLLO DE SOFTWARE")
    print("="*70)
    
    # Crear orquestador
    orchestrator = Orchestrator("Gerente de Proyecto")
    
    # Crear agentes especializados
    print("\n👥 Creando equipo de desarrollo:")
    print("-" * 70)
    
    backend_dev = SpecializedAgent(
        name="Backend Developer",
        specialty="Desarrollo Backend",
        capabilities=["API", "Base de datos", "Seguridad", "Backend"]
    )
    
    frontend_dev = SpecializedAgent(
        name="Frontend Developer",
        specialty="Desarrollo Frontend",
        capabilities=["UI", "UX", "Frontend", "Interfaz"]
    )
    
    tester = SpecializedAgent(
        name="QA Tester",
        specialty="Pruebas y Calidad",
        capabilities=["Testing", "Pruebas", "QA", "Calidad"]
    )
    
    devops = SpecializedAgent(
        name="DevOps Engineer",
        specialty="DevOps e Infraestructura",
        capabilities=["Deploy", "CI/CD", "Infraestructura", "DevOps"]
    )
    
    # Registrar agentes
    print("\n📝 Registrando agentes en el orquestador:")
    orchestrator.register_agent(backend_dev)
    orchestrator.register_agent(frontend_dev)
    orchestrator.register_agent(tester)
    orchestrator.register_agent(devops)
    
    # Definir workflow
    workflow = [
        {
            "type": "Backend",
            "description": "Diseñar y desarrollar una API REST para gestión de usuarios con autenticación JWT"
        },
        {
            "type": "Frontend",
            "description": "Crear interfaz de usuario responsive para el sistema de gestión de usuarios"
        },
        {
            "type": "Testing",
            "description": "Diseñar y ejecutar pruebas de integración para el sistema completo"
        },
        {
            "type": "DevOps",
            "description": "Configurar pipeline de CI/CD y despliegue en ambiente de producción"
        }
    ]
    
    # Ejecutar workflow
    results = orchestrator.execute_workflow(workflow)
    
    # Mostrar resultados
    print(f"\n\n📋 RESUMEN DE RESULTADOS")
    print("=" * 70)
    for i, result in enumerate(results, 1):
        print(f"\nTarea {i}: {result.get('task', 'N/A')[:50]}...")
        print(f"   Agente: {result.get('agent', 'N/A')}")
        print(f"   Estado: {result.get('status', 'N/A')}")
        if result.get('status') == 'completed':
            print(f"   Resultado: {result.get('result', '')[:150]}...")
    
    # Reporte final
    orchestrator.generate_report()


def demo_customer_service():
    """
    Demostración: Sistema de Atención al Cliente
    """
    print("\n\n" + "="*70)
    print("  📞 DEMOSTRACIÓN: CENTRO DE ATENCIÓN AL CLIENTE")
    print("="*70)
    
    # Crear orquestador
    orchestrator = Orchestrator("Coordinador de Servicio")
    
    print("\n👥 Creando equipo de atención:")
    print("-" * 70)
    
    # Crear agentes especializados
    sales_agent = SpecializedAgent(
        name="Agente de Ventas",
        specialty="Ventas y Consultas Comerciales",
        capabilities=["Ventas", "Precios", "Productos", "Cotizaciones"]
    )
    
    support_agent = SpecializedAgent(
        name="Soporte Técnico",
        specialty="Asistencia Técnica",
        capabilities=["Soporte", "Técnico", "Troubleshooting", "Problemas"]
    )
    
    billing_agent = SpecializedAgent(
        name="Agente de Facturación",
        specialty="Facturación y Pagos",
        capabilities=["Facturación", "Pagos", "Contabilidad", "Cobros"]
    )
    
    # Registrar agentes
    orchestrator.register_agent(sales_agent)
    orchestrator.register_agent(support_agent)
    orchestrator.register_agent(billing_agent)
    
    # Simular consultas de clientes
    consultas = [
        {
            "type": "Ventas",
            "description": "Cliente interesado en conocer los planes disponibles y precios para empresas"
        },
        {
            "type": "Soporte",
            "description": "Cliente reporta que no puede acceder a su cuenta, error de autenticación"
        },
        {
            "type": "Facturación",
            "description": "Cliente solicita rectificación de factura del mes pasado por cargos duplicados"
        }
    ]
    
    # Procesar consultas
    results = orchestrator.execute_workflow(consultas)
    
    # Reporte
    orchestrator.generate_report()


def demo_research_collaboration():
    """
    Demostración: Equipo de Investigación Colaborativa
    """
    print("\n\n" + "="*70)
    print("  🔬 DEMOSTRACIÓN: EQUIPO DE INVESTIGACIÓN ACADÉMICA")
    print("="*70)
    
    orchestrator = Orchestrator("Director de Investigación")
    
    print("\n👥 Creando equipo de investigación:")
    print("-" * 70)
    
    # Crear investigadores especializados
    data_analyst = SpecializedAgent(
        name="Analista de Datos",
        specialty="Análisis Estadístico y Data Science",
        capabilities=["Análisis", "Estadística", "Datos", "Visualización"]
    )
    
    literature_reviewer = SpecializedAgent(
        name="Revisor de Literatura",
        specialty="Revisión Bibliográfica",
        capabilities=["Literatura", "Referencias", "Investigación", "Bibliografía"]
    )
    
    writer = SpecializedAgent(
        name="Redactor Científico",
        specialty="Redacción de Papers",
        capabilities=["Redacción", "Escritura", "Paper", "Publicación"]
    )
    
    # Registrar
    orchestrator.register_agent(data_analyst)
    orchestrator.register_agent(literature_reviewer)
    orchestrator.register_agent(writer)
    
    # Workflow de investigación
    research_workflow = [
        {
            "type": "Literatura",
            "description": "Realizar revisión sistemática de literatura sobre aplicaciones de IA en educación (últimos 5 años)"
        },
        {
            "type": "Análisis",
            "description": "Analizar tendencias y patrones en los datos recopilados de los estudios revisados"
        },
        {
            "type": "Redacción",
            "description": "Redactar sección de introducción y estado del arte para paper académico"
        }
    ]
    
    # Ejecutar
    results = orchestrator.execute_workflow(research_workflow)
    orchestrator.generate_report()


if __name__ == "__main__":
    # Ejecutar demostraciones
    demo_software_development_team()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Atención al Cliente...")
    demo_customer_service()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Equipo de Investigación...")
    demo_research_collaboration()
    
    # Lecciones finales
    print("\n\n" + "="*70)
    print("  💡 LECCIONES CLAVE PARA ESTUDIANTES")
    print("="*70)
    print("""
    1. La orquestación permite distribuir tareas según especialización
    2. Cada agente se enfoca en su dominio de experticia
    3. El orquestador coordina y mantiene el flujo de trabajo
    4. Los resultados de un agente pueden alimentar a otros
    5. Este patrón es escalable y permite agregar nuevos agentes fácilmente
    
    💭 Reflexión: ¿Qué otros dominios se beneficiarían de orquestación de agentes?
    """)

