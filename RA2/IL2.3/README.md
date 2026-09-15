# IL2.3: Planificación y Orquestación

## Descripción general

Estrategias de planificación y orquestación para agentes LLM: planificación jerárquica y reactiva, coordinación multi-agente y gestión de flujos con dependencias.

## Objetivos de aprendizaje

- Comparar estrategias de planificación para agentes
- Implementar planificación jerárquica y reactiva
- Diseñar orquestación multi-agente (LangGraph, CrewAI, Python puro; LangChain clásico como contraste)
- Gestionar workflows con dependencias y recursos
- Coordinar y resolver conflictos entre agentes

## Orden sugerido

Ver **[0-guia-pedagogica.md](0-guia-pedagogica.md)** para la secuencia por semanas y el mapa de herramientas (LangGraph vs clásico vs CrewAI vs Python puro).

## ¿Cuáles necesitan API key y cuáles no?

Es la primera pregunta que sale en clase. **Solo 11 de los 24 archivos llaman a un LLM.** El
resto son simulaciones en Python puro: se ejecutan tal cual, sin cuenta de Groq, sin internet y
sin gastar cuota.

| Archivo | ¿Necesita `GROQ_API_KEY`? | Qué usa |
|---|---|---|
| `3-langgraph-planning.py` | **Sí** | LangGraph (`create_agent`) — **camino actual** |
| `3-langgraph-orquestacion.py` | **Sí** | LangGraph (grafo supervisor + especialistas) |
| `4-langgraph-multiagente.ipynb` | **Sí** | LangGraph (supervisor, handoff `Command`, fan-out `Send`) |
| `1-basic_planning.py` | **Sí** | LangChain clásico (ReAct + `AgentExecutor`) |
| `1-langchain_planning.py` | **Sí** | LangChain clásico (ReAct + `AgentExecutor`) |
| `1-basic-planning-agent.ipynb` | **Sí** | LangChain (cadena plan-and-execute) |
| `2-hierarchical-planning.py` | **Sí** | LangChain clásico (ReAct + `AgentExecutor`) |
| `2-crewai_orchestration.py` | **Sí** | CrewAI (prefijo `groq/`) |
| `5-agent-orchestration.py` | **Sí** | Python + `ChatGroq` (orquestación a mano) |
| `7-task-decomposition.py` | **Sí** | LangChain (`ChatGroq`) |
| `Swarm_101.ipynb` | **Sí** | `swarm` (archivada) + Groq |
| `1-planning-strategies.py` | No | Python puro |
| `2-multiagent_orchestration.py` | No | Python puro |
| `3-reactive-planning.py` | No | Python puro |
| `4-goal-oriented-planning.py` | No | Python puro |
| `6-workflow-management.py` | No | Python puro |
| `8-resource-allocation.py` | No | Python puro |
| `9-multi-agent-coordination.py` | No | Python puro |
| `10-conflict-resolution.py` | No | Python puro |
| `11-negotiation-strategies.py` | No | Python puro |
| `12-emergence-behaviors.py` | No | Python puro |
| `_demo_utils.py` | No | Utilidad (no se ejecuta sola) |

> Varios de los archivos "No" llaman igualmente a `load_dotenv()` al arrancar. Es inofensivo:
> cargan el `.env` por costumbre, pero **no** leen `GROQ_API_KEY` ni hacen ninguna petición.
> Si no hay `.env`, funcionan igual.

## Contenido por bloque

### Fundamentos y agentes con LLM (requieren `GROQ_API_KEY` en `.env`)

- [3-langgraph-planning.py](3-langgraph-planning.py) — Café + calculadora con `create_agent` (actual)
- [3-langgraph-orquestacion.py](3-langgraph-orquestacion.py) — Supervisor + especialistas en un grafo
- [4-langgraph-multiagente.ipynb](4-langgraph-multiagente.ipynb) — Supervisor, handoff y fan-out (lo que se usa ahora)
- [4-tendencias-multiagente.md](4-tendencias-multiagente.md) — Criterio de mercado, costos, pauta de proyecto
- [1-basic_planning.py](1-basic_planning.py) — El mismo café, modo clásico (`AgentExecutor`)
- [1-langchain_planning.py](1-langchain_planning.py) — La misma calculadora, modo clásico
- [1-basic-planning-agent.ipynb](1-basic-planning-agent.ipynb) — Notebook de apoyo
- [2-hierarchical-planning.py](2-hierarchical-planning.py) — Planificación jerárquica con LLM
- [2-crewai_orchestration.py](2-crewai_orchestration.py) — Equipo CrewAI (roles, no grafo)
- [5-agent-orchestration.py](5-agent-orchestration.py) — Orquestación a mano con `ChatGroq`
- [7-task-decomposition.py](7-task-decomposition.py) — Descomposición de tareas con LLM

### Planificación y workflows (Python puro, sin API key)

- [1-planning-strategies.py](1-planning-strategies.py) — Comparación de estrategias (Python)
- [2-multiagent_orchestration.py](2-multiagent_orchestration.py) — Coordinación mínima entre dos agentes (Python)
- [3-reactive-planning.py](3-reactive-planning.py) — Planificación reactiva con reglas
- [4-goal-oriented-planning.py](4-goal-oriented-planning.py) — STRIPS / orientada a objetivos
- [6-workflow-management.py](6-workflow-management.py) — DAG, paralelismo y estados de tarea
- [8-resource-allocation.py](8-resource-allocation.py) — Asignación de recursos

### Coordinación avanzada (Python puro, sin API key)

- [9-multi-agent-coordination.py](9-multi-agent-coordination.py) — Coordinación y mensajes
- [10-conflict-resolution.py](10-conflict-resolution.py) — Resolución de conflictos
- [11-negotiation-strategies.py](11-negotiation-strategies.py) — Negociación
- [12-emergence-behaviors.py](12-emergence-behaviors.py) — Comportamientos emergentes

### Otros

- [Swarm_101.ipynb](Swarm_101.ipynb) — Introducción a enfoques tipo swarm.
  **⚠️ Material histórico.** El patrón vigente (ceder el control) está en
  `4-langgraph-multiagente.ipynb` como **handoff** (`Command`). Esta notebook usa la librería
  [`swarm`](https://github.com/openai/swarm), **archivada por OpenAI**: no está en PyPI y
  puede dejar de funcionar sin que cambie nada del curso. Si falla, **no bloquea IL2.3**.
- [_demo_utils.py](_demo_utils.py) — Utilidades para pausas en demos interactivas

### Lecturas

- [4-tendencias-multiagente.md](4-tendencias-multiagente.md)
- [planning-patterns.md](planning-patterns.md)
- [orchestration-guide.md](orchestration-guide.md)
- [coordination-strategies.md](coordination-strategies.md)
- [presentacion.md](presentacion.md)

## Evaluación (referencia)

- Ejercicios prácticos de planificación y orquestación
- Proyecto: sistema multi-agente con flujo no trivial
- Quiz: conceptos de coordinación

## Siguiente: IL2.4

Documenta **este** grafo (nodos, `thread_id`, tokens, por qué no CrewAI).
Plantilla: [`../IL2.4/0-arquitectura-ra2.md`](../IL2.4/0-arquitectura-ra2.md).
Los scripts de IL2.4 no gastan Groq.

## Enlaces útiles

- [LangChain Agents (`create_agent`)](https://docs.langchain.com/oss/python/langchain/agents)
- [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
- [CrewAI](https://docs.crewai.com/)
- [Multi-agent systems (Wikipedia)](https://en.wikipedia.org/wiki/Multi-agent_system)
