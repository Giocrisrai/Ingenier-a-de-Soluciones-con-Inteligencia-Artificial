"""
IL2.3: Asignación Optimizada de Recursos
========================================

Este módulo implementa estrategias de asignación de recursos entre agentes,
optimizando carga de trabajo, tiempo y costos.

Conceptos Clave:
- Balanceo de carga entre agentes
- Optimización de asignación de tareas
- Gestión de capacidades y disponibilidad
- Métricas de rendimiento y utilización
- Algoritmos de scheduling

Para Estudiantes:
La asignación eficiente de recursos es crucial en sistemas multi-agente para
maximizar productividad y minimizar costos. Similar a cómo un manager asigna
tareas a su equipo según capacidades y disponibilidad.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum
import os

from _demo_utils import pause_demo

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv no está instalado")

print("✅ Módulo de asignación de recursos cargado\n")


class ResourceType(Enum):
    """Tipos de recursos"""
    COMPUTE = "compute"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"
    TIME = "time"


@dataclass
class Resource:
    """
    Recurso disponible
    
    Atributos:
        type: Tipo de recurso
        total_capacity: Capacidad total
        available: Capacidad disponible
        unit: Unidad de medida
    """
    type: ResourceType
    total_capacity: float
    available: float
    unit: str
    
    def allocate(self, amount: float) -> bool:
        """Intenta asignar una cantidad del recurso"""
        if amount <= self.available:
            self.available -= amount
            return True
        return False
    
    def release(self, amount: float):
        """Libera una cantidad del recurso"""
        self.available = min(self.available + amount, self.total_capacity)
    
    def utilization(self) -> float:
        """Retorna el porcentaje de utilización"""
        return ((self.total_capacity - self.available) / self.total_capacity) * 100


@dataclass
class Agent:
    """
    Agente con capacidades y recursos
    
    Atributos:
        id: Identificador
        name: Nombre
        skills: Habilidades del agente
        capacity: Capacidad de trabajo (tareas simultáneas)
        current_load: Carga actual
        efficiency: Eficiencia (0.0-1.0)
    """
    id: str
    name: str
    skills: List[str]
    capacity: int
    current_load: int = 0
    efficiency: float = 1.0
    completed_tasks: int = 0
    
    def can_handle(self, task: 'Task') -> bool:
        """Verifica si el agente puede manejar la tarea"""
        has_skills = any(skill in self.skills for skill in task.required_skills)
        has_capacity = self.current_load < self.capacity
        return has_skills and has_capacity
    
    def assign_task(self, task: 'Task'):
        """Asigna una tarea al agente"""
        self.current_load += 1
    
    def complete_task(self, task: 'Task'):
        """Marca una tarea como completada"""
        self.current_load = max(0, self.current_load - 1)
        self.completed_tasks += 1
    
    def utilization(self) -> float:
        """Retorna porcentaje de utilización"""
        return (self.current_load / self.capacity) * 100 if self.capacity > 0 else 0
    
    def is_available(self) -> bool:
        """Verifica si el agente está disponible"""
        return self.current_load < self.capacity


@dataclass
class Task:
    """
    Tarea a asignar
    
    Atributos:
        id: Identificador
        name: Nombre
        required_skills: Habilidades requeridas
        priority: Prioridad (1-10)
        estimated_time: Tiempo estimado en horas
        assigned_to: ID del agente asignado
    """
    id: str
    name: str
    required_skills: List[str]
    priority: int
    estimated_time: float
    assigned_to: str = None
    completed: bool = False


class ResourceAllocator:
    """
    Asignador de recursos y tareas
    
    Atributos:
        agents: Lista de agentes disponibles
        tasks: Cola de tareas pendientes
        allocation_history: Historial de asignaciones
    """
    
    def __init__(self, name: str = "Resource Allocator"):
        self.name = name
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.allocation_history: List[Dict[str, Any]] = []
        
        print(f"🎯 {name} inicializado")
    
    def register_agent(self, agent: Agent):
        """Registra un agente en el sistema"""
        self.agents[agent.id] = agent
        print(f"   ✅ Agente registrado: {agent.name} (Capacidad: {agent.capacity})")
    
    def add_task(self, task: Task):
        """Añade una tarea a la cola"""
        self.tasks[task.id] = task
        print(f"   📝 Tarea añadida: {task.name} (Prioridad: {task.priority})")
    
    def find_best_agent(self, task: Task, strategy: str = "balanced") -> Agent:
        """
        Encuentra el mejor agente para una tarea según estrategia
        
        Args:
            task: Tarea a asignar
            strategy: Estrategia de asignación
                - balanced: Balancea carga entre agentes
                - greedy: Asigna a quien esté más disponible
                - skilled: Prioriza mejor match de habilidades
                - efficient: Prioriza agentes más eficientes
                
        Returns:
            Mejor agente o None
        """
        available_agents = [
            agent for agent in self.agents.values()
            if agent.can_handle(task)
        ]
        
        if not available_agents:
            return None
        
        if strategy == "balanced":
            # Menor utilización
            return min(available_agents, key=lambda a: a.utilization())
        
        elif strategy == "greedy":
            # Mayor disponibilidad
            return max(available_agents, key=lambda a: a.capacity - a.current_load)
        
        elif strategy == "skilled":
            # Mayor número de habilidades coincidentes
            def skill_match(agent):
                return len(set(agent.skills) & set(task.required_skills))
            return max(available_agents, key=skill_match)
        
        elif strategy == "efficient":
            # Mayor eficiencia
            return max(available_agents, key=lambda a: a.efficiency)
        
        else:
            return available_agents[0]
    
    def allocate_task(self, task_id: str, strategy: str = "balanced") -> bool:
        """
        Asigna una tarea a un agente
        
        Args:
            task_id: ID de la tarea
            strategy: Estrategia de asignación
            
        Returns:
            True si se asignó exitosamente
        """
        task = self.tasks.get(task_id)
        if not task or task.assigned_to:
            return False
        
        agent = self.find_best_agent(task, strategy)
        
        if agent is None:
            print(f"   ⚠️ No hay agente disponible para: {task.name}")
            return False
        
        # Asignar
        agent.assign_task(task)
        task.assigned_to = agent.id
        
        # Historial
        self.allocation_history.append({
            "task_id": task.id,
            "task_name": task.name,
            "agent_id": agent.id,
            "agent_name": agent.name,
            "strategy": strategy
        })
        
        print(f"   ✅ Tarea '{task.name}' asignada a {agent.name}")
        return True
    
    def allocate_all(self, strategy: str = "balanced"):
        """
        Asigna todas las tareas pendientes
        
        Args:
            strategy: Estrategia de asignación
        """
        print(f"\n\n{'='*70}")
        print(f"🚀 ASIGNANDO TAREAS (Estrategia: {strategy.upper()})")
        print(f"{'='*70}")
        
        # Ordenar tareas por prioridad
        pending_tasks = [
            t for t in self.tasks.values()
            if not t.assigned_to and not t.completed
        ]
        pending_tasks.sort(key=lambda t: t.priority, reverse=True)
        
        print(f"\nTareas pendientes: {len(pending_tasks)}")
        print(f"Agentes disponibles: {len(self.agents)}")
        
        assigned_count = 0
        for task in pending_tasks:
            if self.allocate_task(task.id, strategy):
                assigned_count += 1
        
        print(f"\n📊 Resultado: {assigned_count}/{len(pending_tasks)} tareas asignadas")
    
    def generate_report(self):
        """Genera reporte de asignación y utilización"""
        print(f"\n\n{'='*70}")
        print(f"📊 REPORTE DE RECURSOS Y ASIGNACIÓN")
        print(f"{'='*70}")
        
        # Estadísticas de agentes
        print(f"\n👥 Utilización de Agentes:")
        for agent in self.agents.values():
            util = agent.utilization()
            bar_length = int(util / 5)
            bar = "█" * bar_length
            print(f"   {agent.name:20} |{bar:20}| {util:5.1f}% ({agent.current_load}/{agent.capacity})")
        
        # Estadísticas de tareas
        total_tasks = len(self.tasks)
        assigned_tasks = sum(1 for t in self.tasks.values() if t.assigned_to)
        unassigned_tasks = total_tasks - assigned_tasks
        
        print(f"\n📋 Estado de Tareas:")
        print(f"   Total: {total_tasks}")
        print(f"   ✅ Asignadas: {assigned_tasks} ({assigned_tasks/total_tasks*100:.1f}%)")
        print(f"   ⏳ Pendientes: {unassigned_tasks} ({unassigned_tasks/total_tasks*100:.1f}%)")
        
        # Distribución de carga
        print(f"\n⚖️  Balance de Carga:")
        avg_load = sum(a.current_load for a in self.agents.values()) / len(self.agents)
        print(f"   Carga promedio: {avg_load:.2f} tareas/agente")
        
        overloaded = [a for a in self.agents.values() if a.current_load > avg_load * 1.2]
        underutilized = [a for a in self.agents.values() if a.current_load < avg_load * 0.8]
        
        if overloaded:
            print(f"   ⚠️ Sobrecargados: {[a.name for a in overloaded]}")
        if underutilized:
            print(f"   ℹ️  Subutilizados: {[a.name for a in underutilized]}")


def demo_software_team():
    """
    Demostración: Equipo de Desarrollo
    """
    print("="*70)
    print("  🎓 DEMOSTRACIÓN: ASIGNACIÓN EN EQUIPO DE DESARROLLO")
    print("="*70)
    
    allocator = ResourceAllocator("Software Team Allocator")
    
    # Crear agentes (desarrolladores)
    print("\n👥 Registrando desarrolladores:")
    
    allocator.register_agent(Agent(
        id="dev1",
        name="Alice (Backend)",
        skills=["Python", "API", "Database"],
        capacity=3,
        efficiency=0.95
    ))
    
    allocator.register_agent(Agent(
        id="dev2",
        name="Bob (Frontend)",
        skills=["React", "CSS", "JavaScript"],
        capacity=3,
        efficiency=0.90
    ))
    
    allocator.register_agent(Agent(
        id="dev3",
        name="Carol (Fullstack)",
        skills=["Python", "React", "API", "Database"],
        capacity=2,
        efficiency=0.85
    ))
    
    allocator.register_agent(Agent(
        id="dev4",
        name="David (DevOps)",
        skills=["Docker", "CI/CD", "Cloud"],
        capacity=4,
        efficiency=0.92
    ))
    
    # Añadir tareas
    print("\n📝 Añadiendo tareas:")
    
    tasks = [
        Task("t1", "Diseñar API REST", ["Python", "API"], 9, 8),
        Task("t2", "Crear componentes UI", ["React", "CSS"], 8, 6),
        Task("t3", "Integrar con BD", ["Python", "Database"], 7, 5),
        Task("t4", "Configurar CI/CD", ["CI/CD", "Docker"], 8, 4),
        Task("t5", "Tests de API", ["Python", "API"], 6, 3),
        Task("t6", "Optimizar queries", ["Database", "Python"], 5, 4),
        Task("t7", "Deploy en Cloud", ["Cloud", "Docker"], 7, 3),
        Task("t8", "Responsive design", ["CSS", "React"], 5, 4),
    ]
    
    for task in tasks:
        allocator.add_task(task)
    
    # Probar diferentes estrategias
    print("\n\n🔄 Probando Estrategia: BALANCED")
    allocator.allocate_all(strategy="balanced")
    allocator.generate_report()
    
    # Reset para probar otra estrategia
    for agent in allocator.agents.values():
        agent.current_load = 0
    for task in allocator.tasks.values():
        task.assigned_to = None
    
    print("\n\n🔄 Probando Estrategia: SKILLED")
    allocator.allocate_all(strategy="skilled")
    allocator.generate_report()


def demo_customer_service():
    """
    Demostración: Centro de Atención al Cliente
    """
    print("\n\n" + "="*70)
    print("  📞 DEMOSTRACIÓN: CENTRO DE ATENCIÓN AL CLIENTE")
    print("="*70)
    
    allocator = ResourceAllocator("Customer Service Allocator")
    
    # Crear agentes
    print("\n👥 Registrando agentes:")
    
    allocator.register_agent(Agent(
        id="agent1",
        name="Ana (Ventas)",
        skills=["Ventas", "Productos", "Cotizaciones"],
        capacity=5
    ))
    
    allocator.register_agent(Agent(
        id="agent2",
        name="Luis (Soporte)",
        skills=["Soporte", "Técnico", "Troubleshooting"],
        capacity=4
    ))
    
    allocator.register_agent(Agent(
        id="agent3",
        name="María (General)",
        skills=["Ventas", "Soporte", "Información"],
        capacity=6
    ))
    
    # Añadir tareas (tickets de clientes)
    print("\n📝 Añadiendo tickets:")
    
    tickets = [
        Task("ticket1", "Consulta de precios", ["Ventas"], 8, 0.5),
        Task("ticket2", "Error de login", ["Soporte", "Técnico"], 9, 1),
        Task("ticket3", "Info de productos", ["Ventas", "Productos"], 6, 0.5),
        Task("ticket4", "Problema de conexión", ["Soporte", "Técnico"], 10, 1.5),
        Task("ticket5", "Solicitud de cotización", ["Ventas", "Cotizaciones"], 7, 1),
        Task("ticket6", "Información general", ["Información"], 5, 0.25),
        Task("ticket7", "Reinstalar app", ["Soporte"], 8, 1),
        Task("ticket8", "Descuentos disponibles", ["Ventas"], 6, 0.5),
    ]
    
    for ticket in tickets:
        allocator.add_task(ticket)
    
    # Asignar
    allocator.allocate_all(strategy="balanced")
    allocator.generate_report()


if __name__ == "__main__":
    # Ejecutar demostraciones
    demo_software_team()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Centro de Atención al Cliente...")
    demo_customer_service()
    
    # Lecciones finales
    print("\n\n" + "="*70)
    print("  💡 LECCIONES CLAVE PARA ESTUDIANTES")
    print("="*70)
    print("""
    1. La asignación eficiente maximiza utilización de recursos
    2. Diferentes estrategias sirven para diferentes objetivos
    3. El balance de carga previene sobrecarga y subutilización
    4. Las habilidades y capacidades deben considerarse en la asignación
    5. Las métricas de utilización ayudan a identificar cuellos de botella
    
    💭 Reflexión: ¿Cómo mejorarías la asignación para manejar prioridades dinámicas?
    """)

