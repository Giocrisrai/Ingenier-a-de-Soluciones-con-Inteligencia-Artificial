"""
IL2.3: Comportamientos Emergentes en Sistemas Multi-Agente
==========================================================

Este módulo explora cómo comportamientos complejos pueden emerger de
interacciones simples entre múltiples agentes, sin control centralizado.

Conceptos Clave:
- Auto-organización
- Comportamientos colectivos
- Patrones emergentes
- Swarm intelligence (inteligencia de enjambre)
- Emergencia vs diseño explícito

Para Estudiantes:
Los comportamientos emergentes son fascinantes: patrones complejos que surgen
de reglas simples. Como bandadas de pájaros, colonias de hormigas, o tráfico
urbano. En IA, esto permite sistemas más robustos y adaptables.
"""

from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
import os
import random
import time

from _demo_utils import pause_demo

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("✅ Módulo de comportamientos emergentes cargado\n")


@dataclass
class Position:
    """Posición en 2D"""
    x: float
    y: float
    
    def distance_to(self, other: 'Position') -> float:
        """Calcula distancia euclidiana a otra posición"""
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
    def move_towards(self, other: 'Position', speed: float):
        """Mueve hacia otra posición"""
        dx = other.x - self.x
        dy = other.y - self.y
        distance = self.distance_to(other)
        
        if distance > 0:
            self.x += (dx / distance) * speed
            self.y += (dy / distance) * speed


class BoidAgent:
    """
    Agente tipo Boid (simulación de bandada)
    
    Implementa tres reglas simples que generan comportamiento de bandada:
    1. Separación: Evitar colisiones con vecinos
    2. Alineación: Moverse en la misma dirección que vecinos
    3. Cohesión: Moverse hacia el centro del grupo
    """
    
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.position = Position(x, y)
        self.velocity = Position(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )
        self.max_speed = 2.0
        self.perception_radius = 50.0
    
    def get_neighbors(self, all_agents: List['BoidAgent']) -> List['BoidAgent']:
        """Encuentra agentes vecinos dentro del radio de percepción"""
        neighbors = []
        for agent in all_agents:
            if agent.id != self.id:
                distance = self.position.distance_to(agent.position)
                if distance < self.perception_radius:
                    neighbors.append(agent)
        return neighbors
    
    def separation(self, neighbors: List['BoidAgent']) -> Tuple[float, float]:
        """Regla 1: Evitar colisiones"""
        steer_x, steer_y = 0.0, 0.0
        
        for neighbor in neighbors:
            distance = self.position.distance_to(neighbor.position)
            if distance < 25:  # Radio de separación
                # Alejarse del vecino
                steer_x += (self.position.x - neighbor.position.x) / distance
                steer_y += (self.position.y - neighbor.position.y) / distance
        
        return steer_x, steer_y
    
    def alignment(self, neighbors: List['BoidAgent']) -> Tuple[float, float]:
        """Regla 2: Alinearse con vecinos"""
        if not neighbors:
            return 0.0, 0.0
        
        avg_vx = sum(n.velocity.x for n in neighbors) / len(neighbors)
        avg_vy = sum(n.velocity.y for n in neighbors) / len(neighbors)
        
        return avg_vx - self.velocity.x, avg_vy - self.velocity.y
    
    def cohesion(self, neighbors: List['BoidAgent']) -> Tuple[float, float]:
        """Regla 3: Moverse hacia el centro del grupo"""
        if not neighbors:
            return 0.0, 0.0
        
        center_x = sum(n.position.x for n in neighbors) / len(neighbors)
        center_y = sum(n.position.y for n in neighbors) / len(neighbors)
        
        return center_x - self.position.x, center_y - self.position.y
    
    def update(self, all_agents: List['BoidAgent'], weights: Dict[str, float]):
        """
        Actualiza posición y velocidad según las tres reglas
        
        Args:
            all_agents: Todos los agentes en el sistema
            weights: Pesos para cada regla (separation, alignment, cohesion)
        """
        neighbors = self.get_neighbors(all_agents)
        
        # Aplicar reglas con pesos
        sep_x, sep_y = self.separation(neighbors)
        ali_x, ali_y = self.alignment(neighbors)
        coh_x, coh_y = self.cohesion(neighbors)
        
        # Combinar fuerzas
        self.velocity.x += (sep_x * weights['separation'] +
                           ali_x * weights['alignment'] +
                           coh_x * weights['cohesion'])
        self.velocity.y += (sep_y * weights['separation'] +
                           ali_y * weights['alignment'] +
                           coh_y * weights['cohesion'])
        
        # Limitar velocidad
        speed = (self.velocity.x**2 + self.velocity.y**2)**0.5
        if speed > self.max_speed:
            self.velocity.x = (self.velocity.x / speed) * self.max_speed
            self.velocity.y = (self.velocity.y / speed) * self.max_speed
        
        # Actualizar posición
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        
        # Wrapping (mundo toroidal)
        self.position.x = self.position.x % 200
        self.position.y = self.position.y % 200


class ForagingAnt:
    """
    Agente hormiga que busca comida y deja feromonas
    
    Demuestra cómo surge comportamiento de forrajeo colectivo.
    """
    
    def __init__(self, id: int, nest_x: float, nest_y: float):
        self.id = id
        self.position = Position(nest_x, nest_y)
        self.nest = Position(nest_x, nest_y)
        self.carrying_food = False
        self.speed = 1.5
        self.random_walk_probability = 0.3
    
    def decide_next_move(self, pheromone_map: Dict[Tuple[int, int], float],
                        food_sources: List[Position]) -> Tuple[float, float]:
        """
        Decide hacia dónde moverse basándose en feromonas
        
        Args:
            pheromone_map: Mapa de feromonas
            food_sources: Ubicaciones de comida
            
        Returns:
            Dirección (dx, dy)
        """
        if self.carrying_food:
            # Regresar al nido
            return self._move_towards(self.nest)
        else:
            # ¿Hay comida cerca?
            for food in food_sources:
                if self.position.distance_to(food) < 5:
                    self.carrying_food = True
                    return 0, 0
            
            # Seguir feromonas o caminar aleatoriamente
            if random.random() < self.random_walk_probability:
                return random.uniform(-1, 1), random.uniform(-1, 1)
            else:
                # Seguir gradiente de feromonas
                return self._follow_pheromones(pheromone_map)
    
    def _move_towards(self, target: Position) -> Tuple[float, float]:
        """Calcula dirección hacia un objetivo"""
        dx = target.x - self.position.x
        dy = target.y - self.position.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 0:
            return dx / distance, dy / distance
        return 0, 0
    
    def _follow_pheromones(self, pheromone_map: Dict[Tuple[int, int], float]) -> Tuple[float, float]:
        """Sigue el gradiente de feromonas"""
        # Simplificado: buscar dirección con más feromonas
        current_pos = (int(self.position.x), int(self.position.y))
        max_pheromone = 0
        best_direction = (random.uniform(-1, 1), random.uniform(-1, 1))
        
        # Revisar 8 direcciones
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor_pos = (current_pos[0] + dx, current_pos[1] + dy)
                pheromone_level = pheromone_map.get(neighbor_pos, 0)
                
                if pheromone_level > max_pheromone:
                    max_pheromone = pheromone_level
                    best_direction = (dx, dy)
        
        return best_direction
    
    def deposit_pheromone(self, pheromone_map: Dict[Tuple[int, int], float]):
        """Deposita feromona en la posición actual"""
        pos = (int(self.position.x), int(self.position.y))
        current = pheromone_map.get(pos, 0)
        pheromone_map[pos] = min(100, current + 10)


class SwarmSimulation:
    """
    Simulación de sistemas multi-agente con comportamientos emergentes
    """
    
    def __init__(self, num_agents: int, simulation_type: str = "boids"):
        self.simulation_type = simulation_type
        self.agents = []
        self.iteration = 0
        
        if simulation_type == "boids":
            # Inicializar agentes boid
            for i in range(num_agents):
                x = random.uniform(0, 200)
                y = random.uniform(0, 200)
                self.agents.append(BoidAgent(i, x, y))
            
            print(f"🦅 Simulación de Bandada creada con {num_agents} agentes")
        
        elif simulation_type == "ants":
            # Inicializar hormigas
            nest_x, nest_y = 100, 100
            for i in range(num_agents):
                self.agents.append(ForagingAnt(i, nest_x, nest_y))
            
            # Crear fuentes de comida
            self.food_sources = [
                Position(150, 150),
                Position(50, 150),
                Position(100, 50)
            ]
            self.pheromone_map = {}
            
            print(f"🐜 Simulación de Hormigas creada con {num_agents} agentes")
    
    def run_iteration(self):
        """Ejecuta una iteración de la simulación"""
        self.iteration += 1
        
        if self.simulation_type == "boids":
            # Actualizar todos los boids
            weights = {
                'separation': 0.15,
                'alignment': 0.1,
                'cohesion': 0.05
            }
            
            for agent in self.agents:
                agent.update(self.agents, weights)
        
        elif self.simulation_type == "ants":
            # Actualizar hormigas
            for ant in self.agents:
                dx, dy = ant.decide_next_move(self.pheromone_map, self.food_sources)
                ant.position.x += dx * ant.speed
                ant.position.y += dy * ant.speed
                
                # Depositar feromona
                if ant.carrying_food:
                    ant.deposit_pheromone(self.pheromone_map)
                
                # Si llegó al nido con comida
                if ant.carrying_food and ant.position.distance_to(ant.nest) < 5:
                    ant.carrying_food = False
            
            # Evaporar feromonas
            self._evaporate_pheromones()
    
    def _evaporate_pheromones(self):
        """Evaporación gradual de feromonas"""
        for pos in list(self.pheromone_map.keys()):
            self.pheromone_map[pos] *= 0.95
            if self.pheromone_map[pos] < 0.1:
                del self.pheromone_map[pos]
    
    def analyze_emergence(self) -> Dict[str, Any]:
        """Analiza patrones emergentes"""
        if self.simulation_type == "boids":
            return self._analyze_flock_behavior()
        elif self.simulation_type == "ants":
            return self._analyze_foraging_behavior()
    
    def _analyze_flock_behavior(self) -> Dict[str, Any]:
        """Analiza comportamiento de bandada"""
        # Centro de masa
        center_x = sum(a.position.x for a in self.agents) / len(self.agents)
        center_y = sum(a.position.y for a in self.agents) / len(self.agents)
        
        # Dispersión
        distances = [a.position.distance_to(Position(center_x, center_y)) 
                    for a in self.agents]
        avg_distance = sum(distances) / len(distances)
        
        # Velocidad promedio
        avg_speed = sum((a.velocity.x**2 + a.velocity.y**2)**0.5 
                       for a in self.agents) / len(self.agents)
        
        return {
            "center": (center_x, center_y),
            "cohesion": avg_distance,
            "avg_speed": avg_speed,
            "num_agents": len(self.agents)
        }
    
    def _analyze_foraging_behavior(self) -> Dict[str, Any]:
        """Analiza comportamiento de forrajeo"""
        carrying_food = sum(1 for ant in self.agents if ant.carrying_food)
        pheromone_trails = len(self.pheromone_map)
        
        return {
            "ants_with_food": carrying_food,
            "pheromone_trails": pheromone_trails,
            "food_sources": len(self.food_sources),
            "num_agents": len(self.agents)
        }


def demo_flocking():
    """
    Demostración: Comportamiento de Bandada (Boids)
    """
    print("="*70)
    print("  🎓 DEMOSTRACIÓN: COMPORTAMIENTO DE BANDADA (BOIDS)")
    print("="*70)
    
    print("""
    Tres reglas simples generan comportamiento complejo de bandada:
    1. Separación: Evitar colisiones con vecinos cercanos
    2. Alineación: Moverse en la misma dirección que vecinos
    3. Cohesión: Mantenerse cerca del centro del grupo
    """)
    
    simulation = SwarmSimulation(num_agents=20, simulation_type="boids")
    
    print("\n🔄 Ejecutando simulación...")
    for i in range(10):
        simulation.run_iteration()
        
        if i % 3 == 0:
            analysis = simulation.analyze_emergence()
            print(f"\nIteración {i+1}:")
            print(f"   Centro de bandada: ({analysis['center'][0]:.1f}, {analysis['center'][1]:.1f})")
            print(f"   Cohesión (dispersión): {analysis['cohesion']:.1f}")
            print(f"   Velocidad promedio: {analysis['avg_speed']:.2f}")
        
        time.sleep(0.1)
    
    print("\n✅ Observación: Sin control central, la bandada mantiene cohesión")
    print("   y se mueve coordinadamente. ¡Comportamiento emergente!")


def demo_ant_foraging():
    """
    Demostración: Forrajeo de Hormigas
    """
    print("\n\n" + "="*70)
    print("  🐜 DEMOSTRACIÓN: FORRAJEO DE HORMIGAS")
    print("="*70)
    
    print("""
    Las hormigas encuentran caminos óptimos a la comida mediante:
    - Exploración aleatoria inicial
    - Depósito de feromonas al encontrar comida
    - Seguimiento de rastros de feromonas
    - Refuerzo de caminos más cortos
    """)
    
    simulation = SwarmSimulation(num_agents=30, simulation_type="ants")
    
    print("\n🔄 Ejecutando simulación de forrajeo...")
    for i in range(15):
        simulation.run_iteration()
        
        if i % 5 == 0:
            analysis = simulation.analyze_emergence()
            print(f"\nIteración {i+1}:")
            print(f"   Hormigas con comida: {analysis['ants_with_food']}")
            print(f"   Rastros de feromona: {analysis['pheromone_trails']}")
            print(f"   Fuentes de comida: {analysis['food_sources']}")
        
        time.sleep(0.1)
    
    print("\n✅ Observación: Las hormigas encuentran caminos eficientes sin")
    print("   planificación central. ¡Inteligencia de enjambre!")


def demo_pattern_formation():
    """
    Demostración: Formación de Patrones
    """
    print("\n\n" + "="*70)
    print("  🌀 DEMOSTRACIÓN: FORMACIÓN DE PATRONES EMERGENTES")
    print("="*70)
    
    print("""
    Principios de emergencia en sistemas multi-agente:
    
    1. REGLAS LOCALES → PATRONES GLOBALES
       - Cada agente sigue reglas simples
       - Patrones complejos emergen de interacciones
    
    2. AUTO-ORGANIZACIÓN
       - No hay control centralizado
       - El orden surge espontáneamente
    
    3. ROBUSTEZ
       - El sistema funciona aunque fallen agentes individuales
       - Adaptabilidad ante cambios
    
    4. ESCALABILIDAD
       - Funciona con 10 o 10,000 agentes
       - Principios se mantienen
    
    Aplicaciones:
    - Optimización de rutas (algoritmos de colonia de hormigas)
    - Robótica de enjambre
    - Sistemas distribuidos
    - Modelado de fenómenos sociales
    """)


if __name__ == "__main__":
    # Ejecutar demostraciones
    demo_flocking()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Forrajeo de Hormigas...")
    demo_ant_foraging()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Principios de Emergencia...")
    demo_pattern_formation()
    
    # Lecciones finales
    print("\n\n" + "="*70)
    print("  💡 LECCIONES CLAVE PARA ESTUDIANTES")
    print("="*70)
    print("""
    1. Comportamientos complejos pueden emerger de reglas simples
    2. No siempre se necesita control centralizado
    3. Los sistemas emergentes son robustos y adaptativos
    4. La inteligencia colectiva supera la individual
    5. La naturaleza ofrece inspiración para algoritmos poderosos
    
    💭 Reflexión: ¿Qué otros sistemas en la naturaleza muestran emergencia?
                 ¿Cómo podrías aplicar estos principios a tus proyectos?
    """)

