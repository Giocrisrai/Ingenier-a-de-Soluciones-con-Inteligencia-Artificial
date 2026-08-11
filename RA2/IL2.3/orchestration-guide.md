# Guía de Orquestación de Agentes

## 📋 Introducción

La orquestación de agentes se refiere a la coordinación y gestión de múltiples agentes especializados trabajando juntos para resolver problemas complejos. Esta guía proporciona mejores prácticas y patrones de implementación.

---

## 🎯 Conceptos Fundamentales

### ¿Qué es la Orquestación?

La orquestación es el proceso de:
- 📌 Coordinar acciones de múltiples agentes
- 📌 Asignar tareas según especialización
- 📌 Gestionar flujo de información
- 📌 Sincronizar resultados
- 📌 Manejar errores y failovers

### Orquestación vs Coreografía

| Aspecto | Orquestación | Coreografía |
|---------|--------------|-------------|
| **Control** | Centralizado | Distribuido |
| **Coordinador** | Sí (Orquestador) | No (Peer-to-peer) |
| **Complejidad** | Media | Alta |
| **Escalabilidad** | Buena | Excelente |
| **Debugging** | Fácil | Difícil |

---

## 🏗️ Arquitecturas de Orquestación

### 1. Orquestación Centralizada

**Estructura**:
```
       [Orquestador]
          /  |  \
         /   |   \
     [A1] [A2] [A3]
```

**Características**:
- Control central de flujo
- Orquestador conoce todos los agentes
- Fácil de mantener y debuggear

**Cuándo usar**:
- ✓ Flujos de trabajo predecibles
- ✓ Necesitas visibilidad completa
- ✓ Número moderado de agentes
- ✓ Tienes infraestructura centralizada

**Implementación básica**:
```python
class Orchestrator:
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent):
        self.agents[agent.id] = agent
    
    def execute_workflow(self, tasks):
        results = []
        for task in tasks:
            agent = self.find_suitable_agent(task)
            result = agent.execute(task)
            results.append(result)
        return results
```

---

### 2. Orquestación Jerárquica

**Estructura**:
```
    [Orquestador Principal]
         /          \
  [Sub-Orq A]  [Sub-Orq B]
    /    \        /    \
  [A1]  [A2]   [B1]  [B2]
```

**Características**:
- Múltiples niveles de coordinación
- Divide responsabilidades
- Escalable para sistemas grandes

**Cuándo usar**:
- ✓ Sistemas muy grandes
- ✓ Dominios separados
- ✓ Necesitas delegar gestión
- ✓ Diferentes equipos/departamentos

---

### 3. Orquestación Distribuida (Coreografía)

**Estructura**:
```
  [A1] ←→ [A2]
   ↕        ↕
  [A3] ←→ [A4]
```

**Características**:
- Sin punto central de control
- Agentes se coordinan directamente
- Mayor autonomía

**Cuándo usar**:
- ✓ Sistemas altamente distribuidos
- ✓ Necesitas máxima escalabilidad
- ✓ Tolerancia a fallos crítica
- ✓ Microservicios

---

## 🔧 Componentes de un Sistema Orquestado

### 1. Agentes Especializados

Cada agente debe tener:
- **Especialización clara**: Un dominio de experticia
- **Capacidades definidas**: Lista de lo que puede hacer
- **Interfaz estándar**: Métodos consistentes
- **Estado independiente**: No depender de otros

**Ejemplo**:
```python
class SpecializedAgent:
    def __init__(self, name, specialty, capabilities):
        self.name = name
        self.specialty = specialty
        self.capabilities = capabilities
    
    def can_handle(self, task):
        return task.type in self.capabilities
    
    def execute(self, task):
        # Lógica específica del agente
        pass
```

### 2. Orquestador

Responsabilidades:
- ✅ Registro de agentes
- ✅ Descubrimiento de capacidades
- ✅ Enrutamiento de tareas
- ✅ Monitoreo de ejecución
- ✅ Manejo de errores

### 3. Cola de Tareas

Gestiona:
- Tareas pendientes
- Priorización
- Retry logic
- Dead letter queue

### 4. Sistema de Mensajería

Facilita:
- Comunicación entre componentes
- Eventos y notificaciones
- Logging centralizado
- Monitoreo

---

## 📊 Patrones de Orquestación

### Patrón 1: Pipeline Secuencial

**Descripción**: Tareas ejecutadas en secuencia, output de una es input de la siguiente.

```
[Tarea 1] → [Tarea 2] → [Tarea 3] → [Resultado]
```

**Ejemplo de uso**:
- ETL (Extract, Transform, Load)
- Procesamiento de imágenes
- Workflows de CI/CD

**Código**:
```python
def pipeline_pattern(tasks, initial_data):
    result = initial_data
    for task in tasks:
        agent = find_agent_for_task(task)
        result = agent.execute(task, result)
    return result
```

---

### Patrón 2: Scatter-Gather

**Descripción**: Distribuye trabajo a múltiples agentes, luego reúne resultados.

```
         [Orquestador]
         /    |    \
      [A1]  [A2]  [A3]
         \    |    /
         [Agregador]
```

**Ejemplo de uso**:
- Búsqueda paralela
- Análisis de múltiples fuentes
- Procesamiento distribuido

**Código**:
```python
def scatter_gather_pattern(task, agents):
    # Scatter
    subtasks = decompose_task(task)
    futures = [agent.execute_async(st) 
               for agent, st in zip(agents, subtasks)]
    
    # Gather
    results = [f.result() for f in futures]
    return aggregate_results(results)
```

---

### Patrón 3: Routing Condicional

**Descripción**: Enruta tareas basándose en condiciones.

```
[Evaluador] → Condición?
              ├─ Si → [Agente A]
              └─ No → [Agente B]
```

**Ejemplo de uso**:
- Clasificación de tickets
- Enrutamiento inteligente
- Decisiones adaptativas

---

### Patrón 4: Compensación/Saga

**Descripción**: Maneja transacciones distribuidas con compensación en caso de error.

```
[T1] → [T2] → [T3] → Error!
 ↓      ↓      ↓
[C1] ← [C2] ← [C3] (Compensación)
```

**Ejemplo de uso**:
- Transacciones distribuidas
- Procesos de negocio críticos
- Sistemas financieros

---

## 🎯 Estrategias de Asignación de Tareas

### 1. Round Robin

Distribuye tareas equitativamente entre agentes.

**Ventajas**: Simple, balanceado
**Desventajas**: Ignora capacidades específicas

### 2. Basada en Capacidades

Asigna según habilidades del agente.

```python
def assign_by_capability(task, agents):
    suitable = [a for a in agents if a.can_handle(task)]
    return suitable[0] if suitable else None
```

### 3. Basada en Carga

Asigna a agente menos ocupado.

```python
def assign_by_load(task, agents):
    return min(agents, key=lambda a: a.current_load)
```

### 4. Basada en Prioridad

Agentes con mayor prioridad reciben tareas primero.

### 5. Híbrida

Combina múltiples factores.

```python
def assign_hybrid(task, agents):
    scores = []
    for agent in agents:
        score = (
            agent.capability_match(task) * 0.4 +
            (1 - agent.load_percentage()) * 0.3 +
            agent.priority * 0.3
        )
        scores.append((agent, score))
    return max(scores, key=lambda x: x[1])[0]
```

---

## 🚀 Mejores Prácticas

### 0. Antes que nada: ¿de verdad necesitas multi-agente?

**La respuesta por defecto es NO.** Un solo agente con varias herramientas bien descritas
resuelve la gran mayoría de los casos, y es más barato, más rápido y muchísimo más fácil de
depurar. Multi-agente es una decisión de arquitectura que **hay que justificar**.

**Lo que cuesta pasar de 1 agente a N:**

| | 1 agente | N agentes |
|---|---|---|
| **Costo** | 1 contexto | cada agente reenvía contexto → crece más que lineal |
| **Latencia** | 1 llamada | en pipeline, las latencias **se suman** |
| **Depuración** | una traza | hay que reconstruir quién dijo qué a quién |
| **Modos de fallo** | alucina | alucina **y** propaga el error a los demás, y puede entrar en bucle |

**Usa multi-agente solo si se cumple alguna de estas:**
- ✓ Los subproblemas necesitan **herramientas o permisos distintos** (y quieres aislarlos:
  que el agente que lee webs no sea el que puede borrar)
- ✓ Hay trabajo **realmente paralelizable** (scatter-gather sobre 20 documentos)
- ✓ Los prompts de sistema son **incompatibles** entre sí y meterlos juntos degrada la calidad
- ✓ El contexto de un solo agente **no cabe** o se degrada por exceso de instrucciones

**Señales de que sobra el multi-agente:**
- ❌ Los agentes solo se pasan texto en línea recta sin decisiones propias → es una **función**
  con varios pasos, no un equipo
- ❌ Todos usan las mismas herramientas y el mismo modelo → solo estás pagando el contexto
  varias veces
- ❌ No sabrías decir qué agente falló cuando el resultado sale mal

> **Regla práctica**: implementa primero la versión de **un agente** y mídela (calidad, tokens,
> latencia). Solo si esa línea base falla en algo concreto, añade el segundo agente — y vuelve
> a medir. Si no mejora, no lo dejes.

### 1. Diseño de Agentes

✅ **Hacer**:
- Agentes con responsabilidad única
- Interfaces claras y consistentes
- Estado mínimo compartido
- Idempotencia cuando sea posible

❌ **Evitar**:
- Agentes monolíticos
- Acoplamiento fuerte
- Estado global compartido
- Lógica duplicada

### 2. Manejo de Errores

```python
class ResilientOrchestrator:
    def execute_with_retry(self, task, agent, max_retries=3):
        for attempt in range(max_retries):
            try:
                return agent.execute(task)
            except TransientError as e:
                if attempt == max_retries - 1:
                    self.handle_failure(task, e)
                else:
                    self.wait_and_retry(attempt)
            except PermanentError as e:
                self.handle_failure(task, e)
                break
```

### 3. Monitoreo y Observabilidad

Implementar:
- 📊 Métricas: Latencia, throughput, tasa de error
- 📝 Logging: Structured logging con trace IDs
- 🔍 Tracing: Seguimiento end-to-end
- 🚨 Alertas: Umbrales y anomalías

### 4. Escalabilidad

Consideraciones:
- Horizontal scaling de agentes
- Load balancing
- Circuit breakers
- Rate limiting

---

## 📈 Métricas de Rendimiento

### Métricas Clave

1. **Tiempo de Respuesta**
   - P50, P95, P99 latency
   - Tiempo por tarea

2. **Throughput**
   - Tareas por segundo
   - Utilización de agentes

3. **Disponibilidad**
   - Uptime de agentes
   - Tasa de éxito

4. **Eficiencia**
   - Utilización de recursos
   - Balance de carga

5. **Costo** (imprescindible con agentes LLM, y la que más se olvida)
   - **Tokens por tarea completa**, no por agente — es la métrica que decide si el
     multi-agente se justifica
   - Costo en $ por tarea, y comparación contra la línea base de **un solo agente**
   - Nº de turnos por conversación (si crece sin control, hay bucle)
   - Presupuesto máximo por tarea, con corte automático al alcanzarlo

---

## 🛠️ Herramientas y Frameworks

### Para Python
- **LangChain**: Orquestación de LLMs
- **CrewAI**: Multi-agent systems
- **Apache Airflow**: Workflow orchestration
- **Celery**: Task queue

### Para Microservicios
- **Kubernetes**: Container orchestration
- **Apache Kafka**: Event streaming
- **RabbitMQ**: Message broker
- **Temporal**: Workflow engine

---

## 📚 Casos de Uso Reales

### 1. E-commerce
```
Orden → [Inventario] → [Pago] → [Fulfillment] → [Notificación]
```

### 2. Procesamiento de Documentos
```
Upload → [OCR] → [Clasificación] → [Extracción] → [Validación] → Storage
```

### 3. Análisis de Datos
```
Raw Data → [Limpieza] → [Transformación] → [Análisis] → [Visualización]
```

---

## 🎓 Ejercicios

### Ejercicio 1
Diseña una arquitectura de orquestación para un sistema de gestión de órdenes de restaurante.

### Ejercicio 2
Implementa un orquestador con manejo de errores y retry logic.

### Ejercicio 3
Compara orquestación centralizada vs distribuida para un sistema de tu elección.

---

## 🔗 Recursos Relacionados

- [planning-patterns.md](planning-patterns.md) - Patrones de planificación
- [coordination-strategies.md](coordination-strategies.md) - Estrategias de coordinación

---

**Autor**: Módulo IL2.3 - Ingeniería de Soluciones con IA  
**Actualizado**: Agosto 2026  
**Licencia**: Uso Educativo

