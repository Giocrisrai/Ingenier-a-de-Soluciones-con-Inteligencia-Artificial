"""
IL2.3: Resolución de Conflictos entre Agentes
============================================

Este módulo implementa estrategias para detectar y resolver conflictos
que surgen cuando múltiples agentes compiten por recursos o tienen
objetivos contradictorios.

Conceptos Clave:
- Detección de conflictos
- Estrategias de resolución (arbitraje, negociación, votación)
- Priorización y mediación
- Compromiso y cooperación
- Prevención de deadlocks

Para Estudiantes:
En sistemas multi-agente, los conflictos son inevitables cuando agentes 
tienen objetivos diferentes o compiten por recursos limitados. Aprender
a resolverlos es crucial para mantener la armonía del sistema.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import os

from _demo_utils import pause_demo

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("✅ Módulo de resolución de conflictos cargado\n")


class ConflictType(Enum):
    """Tipos de conflictos"""
    RESOURCE = "recurso"
    GOAL = "objetivo"
    PRIORITY = "prioridad"
    TEMPORAL = "temporal"


class ResolutionStrategy(Enum):
    """Estrategias de resolución"""
    PRIORITY_BASED = "basada_en_prioridad"
    NEGOTIATION = "negociación"
    ARBITRATION = "arbitraje"
    VOTING = "votación"
    COMPROMISE = "compromiso"
    FIRST_COME = "primero_en_llegar"


@dataclass
class Conflict:
    """
    Representación de un conflicto
    
    Atributos:
        id: Identificador del conflicto
        type: Tipo de conflicto
        agents_involved: IDs de agentes involucrados
        resource: Recurso en disputa (si aplica)
        description: Descripción del conflicto
        severity: Nivel de severidad (1-10)
        resolved: Si está resuelto
    """
    id: str
    type: ConflictType
    agents_involved: List[str]
    resource: Optional[str]
    description: str
    severity: int
    resolved: bool = False
    resolution: Optional[str] = None


@dataclass
class Agent:
    """
    Agente con prioridades y recursos
    
    Atributos:
        id: Identificador
        name: Nombre
        priority: Prioridad global del agente
        resources: Recursos que posee
        requested_resources: Recursos que solicita
    """
    id: str
    name: str
    priority: int
    resources: List[str] = None
    requested_resources: List[str] = None
    
    def __post_init__(self):
        if self.resources is None:
            self.resources = []
        if self.requested_resources is None:
            self.requested_resources = []
    
    def request_resource(self, resource: str):
        """Solicita un recurso"""
        if resource not in self.requested_resources:
            self.requested_resources.append(resource)
    
    def has_resource(self, resource: str) -> bool:
        """Verifica si el agente tiene el recurso"""
        return resource in self.resources
    
    def give_resource(self, resource: str) -> bool:
        """Cede un recurso"""
        if resource in self.resources:
            self.resources.remove(resource)
            return True
        return False


class ConflictResolver:
    """
    Resolvedor de conflictos entre agentes
    
    Atributos:
        name: Nombre del resolvedor
        agents: Diccionario de agentes
        conflicts: Lista de conflictos detectados
        resources: Recursos disponibles en el sistema
    """
    
    def __init__(self, name: str = "Conflict Resolver"):
        self.name = name
        self.agents: Dict[str, Agent] = {}
        self.conflicts: List[Conflict] = []
        self.resources: Dict[str, bool] = {}  # resource_id: available
        self.conflict_counter = 0
        
        print(f"⚖️  {name} inicializado")
    
    def register_agent(self, agent: Agent):
        """Registra un agente en el sistema"""
        self.agents[agent.id] = agent
        print(f"   ✅ Agente '{agent.name}' registrado (Prioridad: {agent.priority})")
    
    def add_resource(self, resource_id: str):
        """Añade un recurso al sistema"""
        self.resources[resource_id] = True  # Disponible
        print(f"   📦 Recurso '{resource_id}' añadido")
    
    def detect_resource_conflict(self, resource: str) -> Optional[Conflict]:
        """
        Detecta conflicto por un recurso
        
        Args:
            resource: ID del recurso
            
        Returns:
            Conflict si hay conflicto, None si no
        """
        # Encontrar agentes que solicitan el mismo recurso
        requesters = [
            agent for agent in self.agents.values()
            if resource in agent.requested_resources
        ]
        
        if len(requesters) > 1:
            self.conflict_counter += 1
            conflict = Conflict(
                id=f"conflict_{self.conflict_counter}",
                type=ConflictType.RESOURCE,
                agents_involved=[a.id for a in requesters],
                resource=resource,
                description=f"Múltiples agentes solicitan '{resource}'",
                severity=len(requesters) * 2
            )
            return conflict
        
        return None
    
    def detect_all_conflicts(self) -> List[Conflict]:
        """Detecta todos los conflictos en el sistema"""
        print(f"\n🔍 Detectando conflictos...")
        
        detected_conflicts = []
        
        # Verificar cada recurso
        for resource in self.resources:
            conflict = self.detect_resource_conflict(resource)
            if conflict:
                detected_conflicts.append(conflict)
                self.conflicts.append(conflict)
                print(f"   ⚠️ Conflicto detectado: {conflict.description}")
                print(f"      Agentes: {', '.join([self.agents[aid].name for aid in conflict.agents_involved])}")
        
        if not detected_conflicts:
            print(f"   ✅ No se detectaron conflictos")
        
        return detected_conflicts
    
    def resolve_by_priority(self, conflict: Conflict):
        """
        Resuelve conflicto basado en prioridad de agentes
        
        Args:
            conflict: Conflicto a resolver
        """
        print(f"\n🎯 Resolviendo por PRIORIDAD: {conflict.description}")
        
        # Obtener agentes involucrados
        involved_agents = [self.agents[aid] for aid in conflict.agents_involved]
        
        # Ordenar por prioridad (mayor prioridad primero)
        involved_agents.sort(key=lambda a: a.priority, reverse=True)
        
        # El agente con mayor prioridad gana el recurso
        winner = involved_agents[0]
        losers = involved_agents[1:]
        
        print(f"   ✅ Ganador: {winner.name} (prioridad: {winner.priority})")
        print(f"   ❌ Perdedores: {', '.join([a.name for a in losers])}")
        
        # Asignar recurso al ganador
        if conflict.resource:
            winner.resources.append(conflict.resource)
            winner.requested_resources.remove(conflict.resource)
            self.resources[conflict.resource] = False
            
            # Remover solicitudes de perdedores
            for loser in losers:
                if conflict.resource in loser.requested_resources:
                    loser.requested_resources.remove(conflict.resource)
        
        conflict.resolved = True
        conflict.resolution = f"Asignado a {winner.name} por prioridad"
    
    def resolve_by_negotiation(self, conflict: Conflict):
        """
        Resuelve conflicto mediante negociación (alternancia)
        
        Args:
            conflict: Conflicto a resolver
        """
        print(f"\n🤝 Resolviendo por NEGOCIACIÓN: {conflict.description}")
        
        involved_agents = [self.agents[aid] for aid in conflict.agents_involved]
        
        # Estrategia: turnos alternados
        print(f"   Estrategia: Turnos alternados")
        print(f"   Turno 1: {involved_agents[0].name}")
        
        if len(involved_agents) > 1:
            print(f"   Próximo turno: {involved_agents[1].name}")
        
        # Asignar recurso temporalmente al primero
        winner = involved_agents[0]
        if conflict.resource:
            winner.resources.append(conflict.resource)
            winner.requested_resources.remove(conflict.resource)
            self.resources[conflict.resource] = False
        
        conflict.resolved = True
        conflict.resolution = f"Asignado a {winner.name} en turno 1, rotará después"
    
    def resolve_by_compromise(self, conflict: Conflict):
        """
        Resuelve conflicto mediante compromiso (división de recursos)
        
        Args:
            conflict: Conflicto a resolver
        """
        print(f"\n🤲 Resolviendo por COMPROMISO: {conflict.description}")
        
        involved_agents = [self.agents[aid] for aid in conflict.agents_involved]
        
        print(f"   Estrategia: Compartir recurso o dividir tiempo")
        
        # Simular división del recurso/tiempo
        for i, agent in enumerate(involved_agents):
            time_share = 100 / len(involved_agents)
            print(f"   {agent.name}: {time_share:.1f}% del tiempo/recurso")
            
            if conflict.resource:
                agent.requested_resources.remove(conflict.resource)
        
        conflict.resolved = True
        conflict.resolution = f"Recurso compartido entre {len(involved_agents)} agentes"
    
    def resolve_by_voting(self, conflict: Conflict):
        """
        Resuelve conflicto mediante votación (todos los agentes votan)
        
        Args:
            conflict: Conflicto a resolver
        """
        print(f"\n🗳️  Resolviendo por VOTACIÓN: {conflict.description}")
        
        involved_agents = [self.agents[aid] for aid in conflict.agents_involved]
        all_agents = list(self.agents.values())
        
        # Simular votos (aleatorio en este ejemplo)
        votes = {agent.id: 0 for agent in involved_agents}
        
        import random
        for voter in all_agents:
            if voter.id not in [a.id for a in involved_agents]:
                vote_for = random.choice(involved_agents)
                votes[vote_for.id] += 1
                print(f"   {voter.name} vota por {vote_for.name}")
        
        # Determinar ganador
        winner_id = max(votes, key=votes.get)
        winner = self.agents[winner_id]
        
        print(f"   ✅ Ganador por votación: {winner.name} ({votes[winner_id]} votos)")
        
        # Asignar recurso
        if conflict.resource:
            winner.resources.append(conflict.resource)
            winner.requested_resources.remove(conflict.resource)
            self.resources[conflict.resource] = False
            
            for agent in involved_agents:
                if agent.id != winner_id and conflict.resource in agent.requested_resources:
                    agent.requested_resources.remove(conflict.resource)
        
        conflict.resolved = True
        conflict.resolution = f"Ganó {winner.name} por votación ({votes[winner_id]} votos)"
    
    def resolve_conflict(self, conflict: Conflict, strategy: ResolutionStrategy):
        """
        Resuelve un conflicto usando la estrategia especificada
        
        Args:
            conflict: Conflicto a resolver
            strategy: Estrategia de resolución
        """
        if strategy == ResolutionStrategy.PRIORITY_BASED:
            self.resolve_by_priority(conflict)
        elif strategy == ResolutionStrategy.NEGOTIATION:
            self.resolve_by_negotiation(conflict)
        elif strategy == ResolutionStrategy.COMPROMISE:
            self.resolve_by_compromise(conflict)
        elif strategy == ResolutionStrategy.VOTING:
            self.resolve_by_voting(conflict)
        else:
            print(f"⚠️ Estrategia no implementada: {strategy}")
    
    def resolve_all_conflicts(self, strategy: ResolutionStrategy):
        """
        Resuelve todos los conflictos detectados
        
        Args:
            strategy: Estrategia de resolución
        """
        print(f"\n\n{'='*70}")
        print(f"⚖️  RESOLUCIÓN DE CONFLICTOS - Estrategia: {strategy.value.upper()}")
        print(f"{'='*70}")
        
        unresolved = [c for c in self.conflicts if not c.resolved]
        
        if not unresolved:
            print("\n✅ No hay conflictos pendientes")
            return
        
        print(f"\nConflictos a resolver: {len(unresolved)}")
        
        for conflict in unresolved:
            self.resolve_conflict(conflict, strategy)
    
    def generate_report(self):
        """Genera reporte de conflictos"""
        print(f"\n\n{'='*70}")
        print(f"📊 REPORTE DE RESOLUCIÓN DE CONFLICTOS")
        print(f"{'='*70}")
        
        total = len(self.conflicts)
        resolved = sum(1 for c in self.conflicts if c.resolved)
        unresolved = total - resolved
        
        print(f"\n📈 Estadísticas:")
        print(f"   Total de conflictos: {total}")
        print(f"   ✅ Resueltos: {resolved} ({resolved/total*100:.1f}%)" if total > 0 else "   ✅ Resueltos: 0")
        print(f"   ⏳ Pendientes: {unresolved}")
        
        # Detalles por conflicto
        if self.conflicts:
            print(f"\n📋 Detalle de Conflictos:")
            for conflict in self.conflicts:
                status = "✅ Resuelto" if conflict.resolved else "⏳ Pendiente"
                print(f"\n   {conflict.id}: {conflict.description}")
                print(f"      Tipo: {conflict.type.value}")
                print(f"      Severidad: {conflict.severity}/10")
                print(f"      Estado: {status}")
                if conflict.resolution:
                    print(f"      Resolución: {conflict.resolution}")
        
        # Estado de recursos
        print(f"\n📦 Estado de Recursos:")
        for resource, available in self.resources.items():
            status = "🟢 Disponible" if available else "🔴 En uso"
            print(f"   {resource}: {status}")
        
        # Estado de agentes
        print(f"\n👥 Estado de Agentes:")
        for agent in self.agents.values():
            print(f"   {agent.name} (Prioridad: {agent.priority})")
            print(f"      Recursos: {', '.join(agent.resources) if agent.resources else 'Ninguno'}")
            print(f"      Solicitudes: {', '.join(agent.requested_resources) if agent.requested_resources else 'Ninguna'}")


def demo_resource_competition():
    """
    Demostración: Competencia por Recursos
    """
    print("="*70)
    print("  🎓 DEMOSTRACIÓN: COMPETENCIA POR RECURSOS")
    print("="*70)
    
    resolver = ConflictResolver("Resource Manager")
    
    # Crear agentes
    print("\n👥 Registrando agentes:")
    
    resolver.register_agent(Agent("a1", "Agente Alpha", priority=10))
    resolver.register_agent(Agent("a2", "Agente Beta", priority=5))
    resolver.register_agent(Agent("a3", "Agente Gamma", priority=7))
    
    # Añadir recursos
    print("\n📦 Añadiendo recursos:")
    resolver.add_resource("GPU_1")
    resolver.add_resource("GPU_2")
    
    # Solicitudes de recursos
    print("\n📝 Agentes solicitando recursos:")
    resolver.agents["a1"].request_resource("GPU_1")
    resolver.agents["a2"].request_resource("GPU_1")
    resolver.agents["a3"].request_resource("GPU_1")
    
    print(f"   Alpha solicita GPU_1")
    print(f"   Beta solicita GPU_1")
    print(f"   Gamma solicita GPU_1")
    
    # Detectar conflictos
    conflicts = resolver.detect_all_conflicts()
    
    # Resolver por prioridad
    resolver.resolve_all_conflicts(ResolutionStrategy.PRIORITY_BASED)
    resolver.generate_report()


def demo_different_strategies():
    """
    Demostración: Comparación de Estrategias
    """
    print("\n\n" + "="*70)
    print("  🔄 DEMOSTRACIÓN: COMPARACIÓN DE ESTRATEGIAS")
    print("="*70)
    
    # Prueba 1: Prioridad
    print("\n\n--- ESCENARIO: Competencia por base de datos ---")
    
    resolver1 = ConflictResolver("DB Manager")
    resolver1.register_agent(Agent("svc1", "Servicio Web", priority=8))
    resolver1.register_agent(Agent("svc2", "Servicio Backend", priority=9))
    resolver1.register_agent(Agent("svc3", "Servicio Analytics", priority=6))
    
    resolver1.add_resource("database_connection")
    
    resolver1.agents["svc1"].request_resource("database_connection")
    resolver1.agents["svc2"].request_resource("database_connection")
    resolver1.agents["svc3"].request_resource("database_connection")
    
    resolver1.detect_all_conflicts()
    resolver1.resolve_all_conflicts(ResolutionStrategy.COMPROMISE)
    resolver1.generate_report()


if __name__ == "__main__":
    # Ejecutar demostraciones
    demo_resource_competition()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Comparación de Estrategias...")
    demo_different_strategies()
    
    # Lecciones finales
    print("\n\n" + "="*70)
    print("  💡 LECCIONES CLAVE PARA ESTUDIANTES")
    print("="*70)
    print("""
    1. Los conflictos son inevitables en sistemas multi-agente
    2. La detección temprana previene deadlocks y problemas mayores
    3. Diferentes estrategias sirven para diferentes situaciones
    4. La prioridad funciona bien cuando hay jerarquías claras
    5. El compromiso y negociación favorecen la cooperación
    
    💭 Reflexión: ¿Qué estrategia usarías para resolver conflictos en tu equipo?
    """)

