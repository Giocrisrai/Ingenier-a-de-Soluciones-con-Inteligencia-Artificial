"""
IL2.3: Estrategias de Negociación entre Agentes
==============================================

Este módulo implementa diferentes estrategias de negociación que los agentes
pueden usar para llegar a acuerdos mutuamente beneficiosos.

Conceptos Clave:
- Protocolos de negociación
- Ofertas y contraofertas
- Utilidad y preferencias
- Zonas de posible acuerdo (ZOPA)
- Estrategias competitivas vs cooperativas

Para Estudiantes:
La negociación es una habilidad fundamental en sistemas multi-agente donde
cada agente tiene sus propios objetivos. Similar a negociaciones del mundo
real: salarios, contratos, recursos compartidos, etc.
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

print("✅ Módulo de negociación cargado\n")


class NegotiationStrategy(Enum):
    """Estrategias de negociación"""
    COMPETITIVE = "competitiva"  # Maximizar beneficio propio
    COOPERATIVE = "cooperativa"  # Maximizar beneficio mutuo
    BALANCED = "balanceada"      # Equilibrio entre ambos
    ADAPTIVE = "adaptativa"      # Se adapta al oponente


class NegotiationStatus(Enum):
    """Estados de negociación"""
    IN_PROGRESS = "en_progreso"
    AGREEMENT = "acuerdo"
    DEADLOCK = "punto_muerto"
    REJECTED = "rechazado"


@dataclass
class Offer:
    """
    Oferta en una negociación
    
    Atributos:
        proposer: ID del agente que propone
        terms: Términos de la oferta
        utility_for_proposer: Utilidad para el proponente
        round_number: Número de ronda
    """
    proposer: str
    terms: Dict[str, Any]
    utility_for_proposer: float
    round_number: int
    
    def __str__(self):
        return f"Oferta R{self.round_number} de {self.proposer}: {self.terms}"


class NegotiatingAgent:
    """
    Agente con capacidades de negociación
    
    Atributos:
        id: Identificador
        name: Nombre
        strategy: Estrategia de negociación
        preferences: Preferencias y prioridades
        reservation_value: Valor mínimo aceptable
        concession_rate: Tasa de concesión (0-1)
    """
    
    def __init__(self, id: str, name: str, strategy: NegotiationStrategy,
                 preferences: Dict[str, float], reservation_value: float):
        self.id = id
        self.name = name
        self.strategy = strategy
        self.preferences = preferences
        self.reservation_value = reservation_value
        self.concession_rate = 0.1
        self.offers_made = []
        self.offers_received = []
        
        print(f"🤝 Agente negociador '{name}' creado")
        print(f"   Estrategia: {strategy.value}")
        print(f"   Valor de reserva: {reservation_value}")
    
    def calculate_utility(self, terms: Dict[str, Any]) -> float:
        """
        Calcula la utilidad de unos términos dados
        
        Args:
            terms: Términos propuestos
            
        Returns:
            Utilidad total (0-100)
        """
        utility = 0
        for key, value in terms.items():
            if key in self.preferences:
                # Utilidad = preferencia * valor normalizado
                utility += self.preferences[key] * float(value) / 100
        
        return min(100, max(0, utility))
    
    def make_offer(self, round_number: int, previous_offer: Optional[Offer] = None) -> Offer:
        """
        Genera una oferta según la estrategia
        
        Args:
            round_number: Número de ronda actual
            previous_offer: Oferta anterior del oponente
            
        Returns:
            Nueva oferta
        """
        if self.strategy == NegotiationStrategy.COMPETITIVE:
            terms = self._make_competitive_offer(round_number, previous_offer)
        elif self.strategy == NegotiationStrategy.COOPERATIVE:
            terms = self._make_cooperative_offer(round_number, previous_offer)
        elif self.strategy == NegotiationStrategy.BALANCED:
            terms = self._make_balanced_offer(round_number, previous_offer)
        else:  # ADAPTIVE
            terms = self._make_adaptive_offer(round_number, previous_offer)
        
        utility = self.calculate_utility(terms)
        offer = Offer(self.id, terms, utility, round_number)
        self.offers_made.append(offer)
        
        return offer
    
    def _make_competitive_offer(self, round_number: int, previous_offer: Optional[Offer]) -> Dict[str, Any]:
        """Oferta competitiva (maximiza beneficio propio)"""
        if round_number == 1:
            # Primera oferta muy favorable para uno mismo
            return {key: 80 for key in self.preferences.keys()}
        else:
            # Pequeña concesión
            if previous_offer:
                terms = {}
                for key in self.preferences.keys():
                    my_last = self.offers_made[-1].terms.get(key, 80)
                    their_last = previous_offer.terms.get(key, 20)
                    # Moverse ligeramente hacia la oferta del oponente
                    terms[key] = my_last - (self.concession_rate * (my_last - their_last))
                return terms
            return {key: 70 for key in self.preferences.keys()}
    
    def _make_cooperative_offer(self, round_number: int, previous_offer: Optional[Offer]) -> Dict[str, Any]:
        """Oferta cooperativa (busca beneficio mutuo)"""
        if round_number == 1:
            # Oferta balanceada desde el inicio
            return {key: 50 for key in self.preferences.keys()}
        else:
            # Mayor concesión
            if previous_offer:
                terms = {}
                for key in self.preferences.keys():
                    my_last = self.offers_made[-1].terms.get(key, 50)
                    their_last = previous_offer.terms.get(key, 50)
                    # Moverse significativamente hacia punto medio
                    terms[key] = (my_last + their_last) / 2
                return terms
            return {key: 50 for key in self.preferences.keys()}
    
    def _make_balanced_offer(self, round_number: int, previous_offer: Optional[Offer]) -> Dict[str, Any]:
        """Oferta balanceada"""
        if round_number == 1:
            return {key: 60 for key in self.preferences.keys()}
        else:
            if previous_offer:
                terms = {}
                concession = 0.15  # Tasa moderada
                for key in self.preferences.keys():
                    my_last = self.offers_made[-1].terms.get(key, 60)
                    their_last = previous_offer.terms.get(key, 40)
                    terms[key] = my_last - (concession * (my_last - their_last))
                return terms
            return {key: 55 for key in self.preferences.keys()}
    
    def _make_adaptive_offer(self, round_number: int, previous_offer: Optional[Offer]) -> Dict[str, Any]:
        """Oferta adaptativa (se adapta al comportamiento del oponente)"""
        if round_number == 1:
            return {key: 60 for key in self.preferences.keys()}
        
        if previous_offer and len(self.offers_received) > 1:
            # Analizar concesiones del oponente
            last_two = self.offers_received[-2:]
            opponent_concession = 0
            for key in self.preferences.keys():
                old_val = last_two[0].terms.get(key, 50)
                new_val = last_two[1].terms.get(key, 50)
                opponent_concession += abs(new_val - old_val)
            
            # Adaptar concesión propia
            self.concession_rate = min(0.3, opponent_concession / 100)
        
        return self._make_balanced_offer(round_number, previous_offer)
    
    def evaluate_offer(self, offer: Offer) -> bool:
        """
        Evalúa si aceptar una oferta
        
        Args:
            offer: Oferta a evaluar
            
        Returns:
            True si acepta, False si rechaza
        """
        utility = self.calculate_utility(offer.terms)
        self.offers_received.append(offer)
        
        # Aceptar si está por encima del valor de reserva
        accept = utility >= self.reservation_value
        
        print(f"   {self.name} evalúa oferta: utilidad={utility:.1f}, reserva={self.reservation_value}")
        print(f"   Decisión: {'✅ ACEPTAR' if accept else '❌ RECHAZAR'}")
        
        return accept


class Negotiation:
    """
    Proceso de negociación entre dos agentes
    
    Atributos:
        agent1: Primer agente
        agent2: Segundo agente
        max_rounds: Número máximo de rondas
        current_round: Ronda actual
        status: Estado de la negociación
        final_agreement: Acuerdo final (si lo hay)
    """
    
    def __init__(self, agent1: NegotiatingAgent, agent2: NegotiatingAgent, max_rounds: int = 10):
        self.agent1 = agent1
        self.agent2 = agent2
        self.max_rounds = max_rounds
        self.current_round = 0
        self.status = NegotiationStatus.IN_PROGRESS
        self.final_agreement: Optional[Offer] = None
        self.negotiation_history = []
        
        print(f"\n💼 Negociación iniciada:")
        print(f"   Participantes: {agent1.name} vs {agent2.name}")
        print(f"   Máx. rondas: {max_rounds}")
    
    def run(self) -> Dict[str, Any]:
        """
        Ejecuta el proceso de negociación
        
        Returns:
            Resultado de la negociación
        """
        print(f"\n{'='*70}")
        print(f"🤝 PROCESO DE NEGOCIACIÓN")
        print(f"{'='*70}")
        
        last_offer_a1 = None
        last_offer_a2 = None
        
        while self.current_round < self.max_rounds and self.status == NegotiationStatus.IN_PROGRESS:
            self.current_round += 1
            print(f"\n--- Ronda {self.current_round} ---")
            
            # Agente 1 hace oferta
            offer_a1 = self.agent1.make_offer(self.current_round, last_offer_a2)
            print(f"📤 {self.agent1.name}: {offer_a1}")
            
            # Agente 2 evalúa
            if self.agent2.evaluate_offer(offer_a1):
                self.status = NegotiationStatus.AGREEMENT
                self.final_agreement = offer_a1
                print(f"\n🎉 ¡ACUERDO ALCANZADO en ronda {self.current_round}!")
                break
            
            # Agente 2 hace contraoferta
            offer_a2 = self.agent2.make_offer(self.current_round, offer_a1)
            print(f"📤 {self.agent2.name}: {offer_a2}")
            
            # Agente 1 evalúa
            if self.agent1.evaluate_offer(offer_a2):
                self.status = NegotiationStatus.AGREEMENT
                self.final_agreement = offer_a2
                print(f"\n🎉 ¡ACUERDO ALCANZADO en ronda {self.current_round}!")
                break
            
            last_offer_a1 = offer_a1
            last_offer_a2 = offer_a2
            
            # Guardar en historial
            self.negotiation_history.append({
                "round": self.current_round,
                "offer_a1": offer_a1,
                "offer_a2": offer_a2
            })
        
        if self.status == NegotiationStatus.IN_PROGRESS:
            self.status = NegotiationStatus.DEADLOCK
            print(f"\n⚠️ PUNTO MUERTO - No se alcanzó acuerdo en {self.max_rounds} rondas")
        
        return self._generate_result()
    
    def _generate_result(self) -> Dict[str, Any]:
        """Genera resultado de la negociación"""
        print(f"\n\n{'='*70}")
        print(f"📊 RESULTADO DE NEGOCIACIÓN")
        print(f"{'='*70}")
        
        result = {
            "status": self.status.value,
            "rounds": self.current_round,
            "agreement": self.final_agreement.terms if self.final_agreement else None,
            "agent1_utility": 0,
            "agent2_utility": 0
        }
        
        print(f"\nEstado: {self.status.value.upper()}")
        print(f"Rondas: {self.current_round}/{self.max_rounds}")
        
        if self.final_agreement:
            util_a1 = self.agent1.calculate_utility(self.final_agreement.terms)
            util_a2 = self.agent2.calculate_utility(self.final_agreement.terms)
            
            result["agent1_utility"] = util_a1
            result["agent2_utility"] = util_a2
            
            print(f"\nAcuerdo final: {self.final_agreement.terms}")
            print(f"\nUtilidades:")
            print(f"   {self.agent1.name}: {util_a1:.1f}")
            print(f"   {self.agent2.name}: {util_a2:.1f}")
            print(f"   Total combinado: {util_a1 + util_a2:.1f}")
        else:
            print(f"\n❌ No se alcanzó acuerdo")
        
        # Análisis de estrategias
        print(f"\nEstrategias usadas:")
        print(f"   {self.agent1.name}: {self.agent1.strategy.value}")
        print(f"   {self.agent2.name}: {self.agent2.strategy.value}")
        
        return result


def demo_competitive_vs_cooperative():
    """
    Demostración: Estrategia Competitiva vs Cooperativa
    """
    print("="*70)
    print("  🎓 DEMOSTRACIÓN: COMPETITIVA VS COOPERATIVA")
    print("="*70)
    
    # Escenario: Negociación de proyecto
    print("\nEscenario: Negociación de términos de proyecto")
    print("Factores: presupuesto, timeline, alcance")
    
    # Agente competitivo
    client = NegotiatingAgent(
        id="client",
        name="Cliente",
        strategy=NegotiationStrategy.COMPETITIVE,
        preferences={"presupuesto": 40, "timeline": 30, "alcance": 30},
        reservation_value=50
    )
    
    # Agente cooperativo
    provider = NegotiatingAgent(
        id="provider",
        name="Proveedor",
        strategy=NegotiationStrategy.COOPERATIVE,
        preferences={"presupuesto": 50, "timeline": 25, "alcance": 25},
        reservation_value=45
    )
    
    # Negociar
    negotiation = Negotiation(client, provider, max_rounds=5)
    result = negotiation.run()
    
    return result


def demo_balanced_negotiation():
    """
    Demostración: Negociación Balanceada
    """
    print("\n\n" + "="*70)
    print("  🤝 DEMOSTRACIÓN: NEGOCIACIÓN BALANCEADA")
    print("="*70)
    
    print("\nEscenario: Negociación salarial")
    print("Factores: salario_base, bonos, vacaciones")
    
    # Ambos agentes usan estrategia balanceada
    employee = NegotiatingAgent(
        id="emp",
        name="Empleado",
        strategy=NegotiationStrategy.BALANCED,
        preferences={"salario_base": 50, "bonos": 30, "vacaciones": 20},
        reservation_value=55
    )
    
    employer = NegotiatingAgent(
        id="empr",
        name="Empleador",
        strategy=NegotiationStrategy.BALANCED,
        preferences={"salario_base": 40, "bonos": 35, "vacaciones": 25},
        reservation_value=50
    )
    
    negotiation = Negotiation(employee, employer, max_rounds=8)
    result = negotiation.run()
    
    return result


def demo_adaptive_strategy():
    """
    Demostración: Estrategia Adaptativa
    """
    print("\n\n" + "="*70)
    print("  🔄 DEMOSTRACIÓN: ESTRATEGIA ADAPTATIVA")
    print("="*70)
    
    print("\nEscenario: Negociación de recursos compartidos")
    print("Factores: tiempo_uso, costo, prioridad")
    
    # Agente competitivo vs adaptativo
    agent_a = NegotiatingAgent(
        id="a",
        name="Agente A (Competitivo)",
        strategy=NegotiationStrategy.COMPETITIVE,
        preferences={"tiempo_uso": 40, "costo": 35, "prioridad": 25},
        reservation_value=52
    )
    
    agent_b = NegotiatingAgent(
        id="b",
        name="Agente B (Adaptativo)",
        strategy=NegotiationStrategy.ADAPTIVE,
        preferences={"tiempo_uso": 35, "costo": 40, "prioridad": 25},
        reservation_value=50
    )
    
    negotiation = Negotiation(agent_a, agent_b, max_rounds=10)
    result = negotiation.run()
    
    return result


if __name__ == "__main__":
    # Ejecutar demostraciones
    demo_competitive_vs_cooperative()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Negociación Balanceada...")
    demo_balanced_negotiation()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Estrategia Adaptativa...")
    demo_adaptive_strategy()
    
    # Lecciones finales
    print("\n\n" + "="*70)
    print("  💡 LECCIONES CLAVE PARA ESTUDIANTES")
    print("="*70)
    print("""
    1. La negociación permite llegar a acuerdos mutuamente beneficiosos
    2. Diferentes estrategias tienen diferentes resultados
    3. La cooperación suele llevar a mejores resultados totales
    4. La competencia puede maximizar beneficio propio pero arriesga el acuerdo
    5. La adaptabilidad permite responder al comportamiento del oponente
    
    💭 Reflexión: ¿En qué situaciones de tu vida usarías cada estrategia?
    """)

