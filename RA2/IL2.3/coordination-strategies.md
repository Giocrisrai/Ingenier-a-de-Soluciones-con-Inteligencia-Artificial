# Estrategias de Coordinación Multi-Agente

## 📋 Introducción

La coordinación es fundamental en sistemas multi-agente donde agentes autónomos deben trabajar juntos hacia objetivos comunes. Esta guía presenta estrategias, protocolos y mejores prácticas para coordinación efectiva.

---

## 🎯 Conceptos Fundamentales

### ¿Qué es la Coordinación?

La coordinación implica:
- 🤝 **Comunicación**: Intercambio de información
- 🎯 **Sincronización**: Alineación de acciones
- 📊 **Compartición de recursos**: Uso eficiente
- 🤔 **Toma de decisiones colectiva**: Consenso
- 🔄 **Adaptación mutua**: Ajustes basados en otros

---

## 💬 Protocolos de Comunicación

### 1. Paso de Mensajes (Message Passing)

**Descripción**: Agentes se comunican mediante envío explícito de mensajes.

**Tipos de mensajes**:
```
REQUEST    - Solicitud de acción/información
INFORM     - Compartir información
QUERY      - Consulta
PROPOSE    - Propuesta
ACCEPT     - Aceptación
REJECT     - Rechazo
RESPONSE   - Respuesta a solicitud
```

**Ejemplo**:
```python
class Message:
    def __init__(self, sender, receiver, type, content):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.content = content
        self.timestamp = time.time()

# Uso
msg = Message("AgentA", "AgentB", "REQUEST", "Dame datos de ventas")
agentB.receive(msg)
```

**Ventajas**:
- ✅ Control explícito
- ✅ Trazabilidad
- ✅ Flexible

**Desventajas**:
- ❌ Overhead de comunicación
- ❌ Puede ser verboso

---

### 2. Pizarra Compartida (Blackboard)

**Descripción**: Espacio compartido donde agentes leen y escriben información.

```
         [BLACKBOARD]
        /    |    |    \
     [A1]  [A2] [A3]  [A4]
```

**Características**:
- Comunicación indirecta
- Desacoplamiento temporal
- Todos pueden leer/escribir

**Ejemplo de uso**:
- Resolución colaborativa de problemas
- Integración de múltiples fuentes
- Sistemas de diagnóstico

**Código**:
```python
class Blackboard:
    def __init__(self):
        self.data = {}
        self.subscribers = {}
    
    def write(self, key, value, author):
        self.data[key] = {
            'value': value,
            'author': author,
            'timestamp': time.time()
        }
        self._notify_subscribers(key)
    
    def read(self, key):
        return self.data.get(key)
    
    def subscribe(self, key, agent):
        if key not in self.subscribers:
            self.subscribers[key] = []
        self.subscribers[key].append(agent)
```

---

### 3. Broadcast

**Descripción**: Un agente envía mensaje a todos los demás.

```
[Sender] ──┬──> [A1]
           ├──> [A2]
           ├──> [A3]
           └──> [A4]
```

**Cuándo usar**:
- Anuncios generales
- Sincronización global
- Diseminación de información

**Ventajas**:
- ✅ Simple
- ✅ Todos reciben info

**Desventajas**:
- ❌ Ineficiente si solo algunos necesitan
- ❌ Sobrecarga de red

---

## 🔄 Mecanismos de Sincronización

### 1. Tokens y Semáforos

**Descripción**: Control de acceso a recursos compartidos.

```python
class ResourceSemaphore:
    def __init__(self, capacity):
        self.capacity = capacity
        self.available = capacity
        self.queue = []
    
    def acquire(self, agent_id):
        if self.available > 0:
            self.available -= 1
            return True
        else:
            self.queue.append(agent_id)
            return False
    
    def release(self, agent_id):
        self.available += 1
        if self.queue:
            next_agent = self.queue.pop(0)
            self.notify(next_agent)
```

---

### 2. Barreras de Sincronización

**Descripción**: Todos los agentes esperan hasta que todos lleguen a un punto.

```python
class Barrier:
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.waiting = set()
    
    def wait(self, agent_id):
        self.waiting.add(agent_id)
        if len(self.waiting) == self.num_agents:
            self._release_all()
            return True
        return False
```

**Ejemplo de uso**:
- Checkpoints en procesos paralelos
- Sincronización de fases
- Espera por todos antes de continuar

---

### 3. Coordinación Temporal

**Descripción**: Sincronización basada en tiempo.

```python
class TemporalCoordinator:
    def schedule_action(self, agent_id, action, timestamp):
        # Programar acción en momento específico
        heapq.heappush(self.schedule, (timestamp, agent_id, action))
    
    def tick(self, current_time):
        # Ejecutar acciones programadas
        while self.schedule and self.schedule[0][0] <= current_time:
            timestamp, agent_id, action = heapq.heappop(self.schedule)
            self.execute(agent_id, action)
```

---

## 🗳️ Toma de Decisiones Colectiva

### 1. Votación Simple

**Descripción**: Cada agente vota, mayoría gana.

```python
def simple_voting(agents, proposal):
    votes = {'yes': 0, 'no': 0, 'abstain': 0}
    
    for agent in agents:
        vote = agent.vote(proposal)
        votes[vote] += 1
    
    return 'yes' if votes['yes'] > votes['no'] else 'no'
```

**Tipos de votación**:
- **Mayoría simple**: > 50%
- **Mayoría absoluta**: ≥ 50%
- **Supermayoría**: ≥ 66%
- **Unanimidad**: 100%

---

### 2. Votación Ponderada

**Descripción**: Votos tienen diferentes pesos.

```python
def weighted_voting(agents, proposal):
    score = 0
    total_weight = sum(a.weight for a in agents)
    
    for agent in agents:
        vote = agent.vote(proposal)  # 1, 0, -1
        score += vote * agent.weight
    
    return score / total_weight
```

**Cuándo usar**:
- Agentes con diferentes niveles de experiencia
- Jerarquías organizacionales
- Sistemas con reputación

---

### 3. Consenso por Convergencia

**Descripción**: Agentes ajustan opiniones hasta llegar a acuerdo.

```python
def consensus_by_convergence(agents, iterations=10):
    for _ in range(iterations):
        for agent in agents:
            neighbor_opinions = [n.opinion for n in agent.neighbors]
            agent.opinion = agent.update_opinion(neighbor_opinions)
        
        if all_opinions_converged(agents):
            break
    
    return average_opinion(agents)
```

---

### 4. Liderazgo Delegado

**Descripción**: Un líder toma decisiones por el grupo.

```python
class LeaderBasedDecision:
    def __init__(self, agents):
        self.leader = self.elect_leader(agents)
        self.followers = [a for a in agents if a != self.leader]
    
    def decide(self, problem):
        # Recolectar inputs
        inputs = [a.provide_input(problem) for a in self.followers]
        
        # Líder decide
        decision = self.leader.decide(problem, inputs)
        
        return decision
```

---

## 🔀 Estrategias de Coordinación

### 1. Coordinación Reactiva

**Descripción**: Agentes reaccionan a acciones de otros sin planificación previa.

**Principios**:
- Reglas locales simples
- Respuesta inmediata
- Sin modelo global

**Ejemplo - Evitación de colisiones**:
```python
def reactive_coordination(agent, neighbors):
    for neighbor in neighbors:
        if agent.distance_to(neighbor) < SAFETY_RADIUS:
            agent.move_away_from(neighbor)
```

**Ventajas**:
- ✅ Rápido
- ✅ Escalable
- ✅ Robusto

**Desventajas**:
- ❌ Sin optimización global
- ❌ Puede entrar en ciclos

---

### 2. Coordinación Basada en Planes

**Descripción**: Agentes crean y comparten planes, coordinan para evitar conflictos.

**Proceso**:
1. Cada agente crea plan individual
2. Comparten planes
3. Detectan conflictos
4. Ajustan planes
5. Ejecutan coordinadamente

```python
class PlanBasedCoordination:
    def coordinate(self, agents):
        plans = [a.create_plan() for a in agents]
        conflicts = self.detect_conflicts(plans)
        
        while conflicts:
            resolved_plans = self.resolve_conflicts(plans, conflicts)
            plans = resolved_plans
            conflicts = self.detect_conflicts(plans)
        
        return plans
```

---

### 3. Coordinación por Contratos

**Descripción**: Agentes negocian contratos para distribución de tareas.

**Protocolo Contract Net**:
```
Manager → [Announce Task]
         ↓
Contractors → [Submit Bids]
         ↓
Manager → [Award Contract]
         ↓
Winner → [Execute Task]
         ↓
Winner → [Report Results]
```

**Implementación**:
```python
class ContractNet:
    def announce_task(self, task):
        bids = []
        for agent in self.contractors:
            bid = agent.submit_bid(task)
            if bid:
                bids.append((agent, bid))
        
        # Seleccionar mejor oferta
        winner = min(bids, key=lambda x: x[1].cost)
        self.award_contract(winner[0], task)
```

**Cuándo usar**:
- Distribución dinámica de tareas
- Optimización de recursos
- Mercados de tareas

---

### 4. Coordinación por Roles

**Descripción**: Agentes asumen roles específicos con responsabilidades definidas.

**Roles comunes**:
- **Coordinador**: Gestiona flujo
- **Ejecutor**: Realiza tareas
- **Monitor**: Supervisa progreso
- **Mediador**: Resuelve conflictos

```python
class RoleBasedCoordination:
    def assign_roles(self, agents, task):
        roles = {
            'coordinator': self.select_coordinator(agents),
            'executors': self.select_executors(agents, task),
            'monitor': self.select_monitor(agents)
        }
        return roles
```

---

## 🤝 Compartición de Conocimiento

### 1. Broadcast de Descubrimientos

```python
def share_discovery(agent, discovery):
    for neighbor in agent.neighbors:
        neighbor.receive_knowledge(discovery)
```

### 2. Base de Conocimiento Compartida

```python
class SharedKnowledgeBase:
    def __init__(self):
        self.facts = {}
        self.contributors = {}
    
    def add_fact(self, fact, agent_id):
        self.facts[fact.id] = fact
        self.contributors[fact.id] = agent_id
    
    def query(self, condition):
        return [f for f in self.facts.values() if condition(f)]
```

### 3. Aprendizaje Distribuido

Agentes aprenden de experiencias colectivas.

---

## 🎯 Patrones de Coordinación Avanzados

### 1. Formación y Mantenimiento

**Uso**: Robots en formación, drones coordinados

```python
class FormationController:
    def maintain_formation(self, agents, formation_type):
        center = calculate_center(agents)
        
        for i, agent in enumerate(agents):
            target_pos = calculate_formation_position(
                center, formation_type, i, len(agents)
            )
            agent.move_towards(target_pos)
```

---

### 2. Coordinación Emergente

**Descripción**: Patrones globales emergen de interacciones locales.

Ejemplos naturales:
- Bandadas de pájaros
- Colonias de hormigas
- Cardúmenes de peces

---

### 3. Coaliciones Dinámicas

**Descripción**: Agentes forman grupos temporales para tareas específicas.

```python
class Coalition:
    def __init__(self, agents, objective):
        self.members = agents
        self.objective = objective
        self.leader = self.elect_leader()
    
    def can_achieve_alone(self, task):
        total_capability = sum(m.capability for m in self.members)
        return total_capability >= task.requirement
```

---

## 📊 Métricas de Coordinación

### Métricas Clave

1. **Eficiencia de Comunicación**
   - Mensajes por tarea
   - Latencia de comunicación
   - Ancho de banda usado

2. **Calidad de Coordinación**
   - Conflictos evitados
   - Sincronización lograda
   - Objetivos alcanzados

3. **Costo de Coordinación**
   - Overhead computacional
   - Tiempo en coordinación vs ejecución
   - Recursos consumidos

---

## 🚨 Problemas Comunes y Soluciones

### 1. Deadlock

**Problema**: Agentes esperan mutuamente sin progresar.

**Solución**:
- Timeouts
- Detección de ciclos
- Priorización

```python
def detect_deadlock(agents):
    waiting_graph = build_waiting_graph(agents)
    return has_cycle(waiting_graph)
```

---

### 2. Livelock

**Problema**: Agentes activos pero sin progresar.

**Solución**:
- Randomización
- Backoff exponencial
- Cambio de estrategia

---

### 3. Starvation

**Problema**: Algunos agentes nunca obtienen recursos.

**Solución**:
- Fairness algorithms
- Aging (incremento de prioridad)
- Resource reservations

---

## ⚠️ Problemas específicos cuando los agentes son LLM

Deadlock, livelock y starvation vienen de la teoría clásica de sistemas multi-agente (robots,
procesos). Cuando cada "agente" es una **llamada a un LLM**, aparecen otros fallos que el resto
de esta guía no cubre y que son los que de verdad rompen los proyectos:

### 4. Bucle infinito de conversación

**Problema**: A pide aclaración a B, B pide aclaración a A, y así indefinidamente. Ninguno
está bloqueado (no es deadlock) y ambos "progresan" generando texto — pero la tarea no avanza
y **cada vuelta cuesta tokens**.

**Solución** — nunca se confía en que el sistema converja solo:
- **Tope duro de iteraciones** (`max_iter`) y de turnos por conversación
- **Presupuesto de tokens/costo** por tarea: al agotarlo, se corta y se devuelve lo que haya
- **Detección de repetición**: si dos turnos consecutivos son casi idénticos, cortar
- Un **criterio de terminación explícito**, no "hasta que estén de acuerdo"

### 5. Propagación de errores y alucinaciones

**Problema**: el agente A inventa un dato. B lo recibe como hecho, razona sobre él y lo pasa a
C. El error no se detecta: se **amplifica** y, peor, gana apariencia de consenso porque tres
agentes lo repiten. En un pipeline secuencial no hay ningún punto donde alguien verifique.

**Solución**:
- **Validar entre etapas**, no solo al final (esquemas, rangos, chequeos deterministas)
- Marcar la **procedencia** de cada dato: qué agente lo produjo y de qué fuente
- Un agente **verificador** con acceso a la fuente original, no al resumen del anterior
- Que el acuerdo entre agentes **no cuente como evidencia**: N agentes con el mismo modelo y
  el mismo contexto se equivocan de la misma forma

### 6. Costo y latencia se multiplican

**Problema**: pasar de 1 a 5 agentes no cuesta 5×. Cada agente reenvía contexto acumulado, y
en un pipeline secuencial las **latencias se suman**. Es fácil terminar con un sistema 10×
más caro y 5× más lento que un solo agente bien diseñado, para la misma calidad.

**Solución**:
- Medir **tokens y segundos por tarea completa**, no por agente
- Comparar siempre contra la **línea base de un agente único** antes de dar por buena la
  arquitectura multi-agente
- Paralelizar lo que no tenga dependencias (scatter-gather) en vez de encadenar
- Usar el modelo grande solo donde hace falta; los roles simples pueden ir en uno pequeño

### 7. Observabilidad: no sabes cuál agente falló

**Problema**: el resultado final es malo. ¿Falló A, o A estuvo bien y B lo malinterpretó? Sin
trazas no hay forma de saberlo, y como el LLM no es determinista, **no puedes reproducir el
fallo re-ejecutando**.

**Solución**:
- **`trace_id` único** por tarea, propagado a todos los agentes
- Guardar prompt de entrada y salida **de cada agente**, no solo el resultado final
- Registrar tokens, latencia y errores por agente (ver RA3/IL3.1 y IL3.2)
- Fijar `temperature=0` y guardar las semillas mientras se depura

### 8. Seguridad: un agente comprometido contamina al resto

**Problema**: si un agente recibe contenido malicioso (una inyección indirecta dentro de un
documento, una web o la salida de una herramienta), su respuesta pasa a los demás **como si
fuera confiable**. Los mensajes entre agentes normalmente no se validan: la confianza mutua es
justo lo que el atacante aprovecha. En una cadena de delegación, basta comprometer al eslabón
más débil para mover a todo el equipo.

**Solución**:
- Tratar el mensaje de otro agente como **entrada no confiable**, igual que la de un usuario
- **Mínimo privilegio por agente**: que el que lee webs no sea el que puede borrar o pagar
- No propagar credenciales por la cadena de delegación
- Aprobación humana antes de cualquier acción irreversible, sea cual sea el agente que la pida

> Referencia: [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
> — cubre justamente esto: secuestro de objetivo (ASI01), abuso de herramientas (ASI02), abuso
> de identidad y privilegios en cadenas de delegación (ASI03), envenenamiento de memoria y
> contexto (ASI06), comunicación insegura entre agentes (ASI07) y fallos en cascada (ASI08).

---

## 🎓 Ejercicios Prácticos

### Ejercicio 1: Protocolo de Comunicación
Diseña un protocolo de mensajes para un sistema de gestión de inventario multi-almacén.

### Ejercicio 2: Algoritmo de Consenso
Implementa votación ponderada donde el peso depende de la precisión histórica del agente.

### Ejercicio 3: Coordinación Reactiva
Crea reglas reactivas para robots que deben recolectar objetos sin colisionar.

---

## 📚 Referencias

1. **FIPA Standards** - Foundation for Intelligent Physical Agents
2. **Contract Net Protocol** - Smith, 1980
3. **BDI Architecture** - Belief-Desire-Intention
4. **Swarm Intelligence** - Bonabeau et al.

---

## 🔗 Recursos Relacionados

- [planning-patterns.md](planning-patterns.md) - Patrones de planificación
- [orchestration-guide.md](orchestration-guide.md) - Guía de orquestación

---

**Autor**: Módulo IL2.3 - Ingeniería de Soluciones con IA  
**Actualizado**: Agosto 2026  
**Licencia**: Uso Educativo

