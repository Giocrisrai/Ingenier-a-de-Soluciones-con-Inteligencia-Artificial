"""
IL2.3: Planificación Reactiva con Reglas
=======================================

Este módulo demuestra la planificación reactiva, donde el agente responde
dinámicamente a cambios en el entorno usando reglas if-then.

Conceptos Clave:
- Respuesta inmediata a cambios del entorno
- Sistema de reglas (condición → acción)
- Monitoreo continuo de estados
- Adaptación sin re-planificación completa

Para Estudiantes:
La planificación reactiva es útil cuando necesitas responder rápidamente a 
eventos imprevistos. Por ejemplo, un robot que evita obstáculos o un sistema
de alertas que responde a cambios en tiempo real.
"""

# Requiere: pip install langchain langchain-openai openai python-dotenv
from langchain_openai import ChatOpenAI
from typing import Dict, List, Callable, Any
import os
import time
import random

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

# Nota: El LLM se configura como referencia para extensiones futuras,
# pero no se usa en esta demostración standalone de planificación reactiva.
# llm = ChatOpenAI(
#     model="gpt-4o",
#     base_url=github_base_url,
#     api_key=github_token,
#     temperature=0.7
# )

print("✅ Módulo de planificación reactiva cargado")


class ReactiveAgent:
    """
    Agente Reactivo que responde a cambios del entorno mediante reglas
    
    Atributos:
        name: Nombre del agente
        state: Estado actual del entorno
        rules: Reglas de reacción (condición → acción)
        history: Historial de acciones tomadas
    """
    
    def __init__(self, name: str):
        self.name = name
        self.state = {}
        self.rules = []
        self.history = []
        print(f"🤖 Agente Reactivo '{name}' creado")
    
    def add_rule(self, condition: Callable, action: Callable, description: str):
        """
        Añade una regla de reacción al agente
        
        Args:
            condition: Función que evalúa si se cumple la condición
            action: Función que ejecuta la acción
            description: Descripción de la regla
        """
        self.rules.append({
            "condition": condition,
            "action": action,
            "description": description
        })
        print(f"   ✅ Regla añadida: {description}")
    
    def update_state(self, new_state: Dict[str, Any]):
        """
        Actualiza el estado del entorno
        
        Args:
            new_state: Nuevo estado a aplicar
        """
        old_state = self.state.copy()
        self.state.update(new_state)
        
        # Mostrar cambios
        print(f"\n📊 Estado actualizado:")
        for key, value in new_state.items():
            old_val = old_state.get(key, "N/A")
            print(f"   {key}: {old_val} → {value}")
    
    def react(self):
        """
        Evalúa las reglas y ejecuta acciones si se cumplen las condiciones
        
        Returns:
            Lista de acciones ejecutadas
        """
        actions_taken = []
        
        print(f"\n🔍 {self.name} evaluando reglas...")
        
        for i, rule in enumerate(self.rules, 1):
            try:
                if rule["condition"](self.state):
                    print(f"\n   ⚡ Regla {i} activada: {rule['description']}")
                    result = rule["action"](self.state)
                    actions_taken.append({
                        "rule": rule["description"],
                        "result": result,
                        "timestamp": time.time()
                    })
                    print(f"   ✅ Acción ejecutada: {result}")
                    
                    # Agregar al historial
                    self.history.append({
                        "state": self.state.copy(),
                        "rule": rule["description"],
                        "action": result
                    })
            except Exception as e:
                print(f"   ⚠️ Error en regla {i}: {e}")
        
        if not actions_taken:
            print("   ℹ️  No hay reglas que activar en el estado actual")
        
        return actions_taken
    
    def show_history(self):
        """Muestra el historial de reacciones del agente"""
        print(f"\n📜 Historial de {self.name}:")
        print("=" * 60)
        for i, entry in enumerate(self.history, 1):
            print(f"\n{i}. Regla: {entry['rule']}")
            print(f"   Estado: {entry['state']}")
            print(f"   Acción: {entry['action']}")


class EnvironmentSimulator:
    """
    Simulador de entorno que genera cambios aleatorios
    
    Atributos:
        variables: Variables del entorno a simular
        ranges: Rangos válidos para cada variable
    """
    
    def __init__(self):
        self.variables = ["temperatura", "humedad", "presion", "luz"]
        self.ranges = {
            "temperatura": (15, 35),
            "humedad": (30, 90),
            "presion": (950, 1050),
            "luz": (0, 1000)
        }
    
    def generate_state(self) -> Dict[str, float]:
        """
        Genera un estado aleatorio del entorno
        
        Returns:
            Diccionario con valores de las variables
        """
        state = {}
        for var in self.variables:
            min_val, max_val = self.ranges[var]
            state[var] = round(random.uniform(min_val, max_val), 2)
        return state
    
    def simulate_change(self, current_state: Dict[str, float]) -> Dict[str, float]:
        """
        Simula un pequeño cambio en el estado actual
        
        Args:
            current_state: Estado actual
            
        Returns:
            Nuevo estado con cambios
        """
        new_state = current_state.copy()
        # Cambiar aleatoriamente 1-2 variables
        vars_to_change = random.sample(self.variables, random.randint(1, 2))
        
        for var in vars_to_change:
            min_val, max_val = self.ranges[var]
            # Cambio pequeño
            change = random.uniform(-5, 5)
            new_value = current_state.get(var, 20) + change
            # Mantener en rango
            new_state[var] = round(max(min_val, min(max_val, new_value)), 2)
        
        return new_state


def demo_basic_reactive():
    """
    Demostración básica de planificación reactiva
    """
    print("\n" + "="*70)
    print("  🎓 DEMOSTRACIÓN: PLANIFICACIÓN REACTIVA BÁSICA")
    print("="*70)
    
    # Crear agente reactivo
    agent = ReactiveAgent("Monitor de Clima")
    
    # Definir reglas de reacción
    print("\n📋 Definiendo reglas de reacción:")
    
    # Regla 1: Temperatura alta
    agent.add_rule(
        condition=lambda s: s.get("temperatura", 0) > 30,
        action=lambda s: f"Activar aire acondicionado (temp: {s.get('temperatura')}°C)",
        description="Si temperatura > 30°C → Activar A/C"
    )
    
    # Regla 2: Humedad alta
    agent.add_rule(
        condition=lambda s: s.get("humedad", 0) > 70,
        action=lambda s: f"Activar deshumidificador (humedad: {s.get('humedad')}%)",
        description="Si humedad > 70% → Activar deshumidificador"
    )
    
    # Regla 3: Luz baja
    agent.add_rule(
        condition=lambda s: s.get("luz", 1000) < 200,
        action=lambda s: f"Encender luces (luminosidad: {s.get('luz')} lux)",
        description="Si luz < 200 lux → Encender luces"
    )
    
    # Regla 4: Presión baja
    agent.add_rule(
        condition=lambda s: s.get("presion", 1000) < 980,
        action=lambda s: f"Alerta de tormenta (presión: {s.get('presion')} hPa)",
        description="Si presión < 980 hPa → Alerta de tormenta"
    )
    
    # Simular diferentes estados
    print("\n\n🌡️ Simulando diferentes estados del entorno:")
    print("=" * 70)
    
    scenarios = [
        {"temperatura": 32, "humedad": 65, "luz": 500, "presion": 1010},
        {"temperatura": 28, "humedad": 75, "luz": 150, "presion": 975},
        {"temperatura": 35, "humedad": 80, "luz": 100, "presion": 960},
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n\n--- Escenario {i} ---")
        agent.update_state(scenario)
        agent.react()
        time.sleep(0.5)
    
    # Mostrar historial
    agent.show_history()


def demo_smart_home():
    """
    Demostración de casa inteligente con agente reactivo
    """
    print("\n\n" + "="*70)
    print("  🏠 DEMOSTRACIÓN: CASA INTELIGENTE CON IA REACTIVA")
    print("="*70)
    
    # Crear agente para casa inteligente
    smart_home = ReactiveAgent("Casa Inteligente")
    
    print("\n🏠 Configurando sistema de automatización:")
    
    # Reglas de seguridad
    smart_home.add_rule(
        condition=lambda s: s.get("movimiento_detectado") and not s.get("persona_autorizada"),
        action=lambda s: "🚨 Activar alarma de seguridad y notificar propietario",
        description="Movimiento no autorizado → Activar alarma"
    )
    
    # Reglas de eficiencia energética
    smart_home.add_rule(
        condition=lambda s: s.get("habitacion_vacia") and s.get("luces_encendidas"),
        action=lambda s: "💡 Apagar luces para ahorrar energía",
        description="Habitación vacía con luces → Apagar luces"
    )
    
    # Reglas de confort
    smart_home.add_rule(
        condition=lambda s: s.get("hora") >= 22 and s.get("volumen_tv") > 50,
        action=lambda s: "🔇 Reducir volumen (modo nocturno)",
        description="Después de 22h con TV alto → Reducir volumen"
    )
    
    # Reglas de clima
    smart_home.add_rule(
        condition=lambda s: s.get("ventanas_abiertas") and s.get("lloviendo"),
        action=lambda s: "🪟 Cerrar ventanas automáticamente",
        description="Lluvia con ventanas abiertas → Cerrar ventanas"
    )
    
    # Simular situaciones
    situaciones = [
        {
            "escenario": "Intrusión detectada",
            "estado": {"movimiento_detectado": True, "persona_autorizada": False}
        },
        {
            "escenario": "Ahorro energético",
            "estado": {"habitacion_vacia": True, "luces_encendidas": True}
        },
        {
            "escenario": "Modo nocturno",
            "estado": {"hora": 23, "volumen_tv": 70}
        },
        {
            "escenario": "Protección contra lluvia",
            "estado": {"ventanas_abiertas": True, "lloviendo": True}
        }
    ]
    
    for i, sit in enumerate(situaciones, 1):
        print(f"\n\n{'='*70}")
        print(f"Situación {i}: {sit['escenario']}")
        print('='*70)
        smart_home.update_state(sit["estado"])
        smart_home.react()
        time.sleep(0.5)


def demo_continuous_monitoring():
    """
    Demostración de monitoreo continuo con cambios dinámicos
    """
    print("\n\n" + "="*70)
    print("  🔄 DEMOSTRACIÓN: MONITOREO CONTINUO")
    print("="*70)
    
    # Crear agente y simulador
    monitor = ReactiveAgent("Monitor Ambiental")
    simulator = EnvironmentSimulator()
    
    print("\n🎛️ Configurando sistema de monitoreo:")
    
    # Reglas de monitoreo
    monitor.add_rule(
        condition=lambda s: s.get("temperatura", 0) > 32,
        action=lambda s: "🔥 Alerta: Temperatura crítica",
        description="Temperatura crítica"
    )
    
    monitor.add_rule(
        condition=lambda s: s.get("humedad", 0) > 80,
        action=lambda s: "💧 Alerta: Humedad excesiva",
        description="Humedad excesiva"
    )
    
    print("\n\n🔄 Iniciando monitoreo continuo (5 ciclos):")
    print("=" * 70)
    
    # Estado inicial
    current_state = simulator.generate_state()
    monitor.update_state(current_state)
    
    # Ciclos de monitoreo
    for cycle in range(1, 6):
        print(f"\n\n--- Ciclo {cycle} ---")
        
        # Simular cambio en el entorno
        new_state = simulator.simulate_change(current_state)
        monitor.update_state(new_state)
        
        # Reaccionar a cambios
        monitor.react()
        
        current_state = new_state
        time.sleep(0.3)
    
    print("\n\n✅ Monitoreo completado")


if __name__ == "__main__":
    # Ejecutar demostraciones
    demo_basic_reactive()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para continuar con Casa Inteligente...")
    demo_smart_home()
    
    print("\n\n" + "="*70)
    pause_demo("Presiona ENTER para ver Monitoreo Continuo...")
    demo_continuous_monitoring()
    
    # Lecciones finales
    print("\n\n" + "="*70)
    print("  💡 LECCIONES CLAVE PARA ESTUDIANTES")
    print("="*70)
    print("""
    1. La planificación reactiva es ideal para entornos dinámicos e impredecibles
    2. Las reglas if-then permiten respuestas rápidas sin re-planificación
    3. Es importante definir reglas claras y no contradictorias
    4. El monitoreo continuo permite adaptación en tiempo real
    5. Este enfoque es eficiente pero puede ser limitado en problemas complejos
    
    💭 Reflexión: ¿Cuándo usarías planificación reactiva vs jerárquica?
    """)

