# IL2.3: Planificación y Orquestación

## Descripción general

Estrategias de planificación y orquestación para agentes LLM: planificación jerárquica y reactiva, coordinación multi-agente y gestión de flujos con dependencias.

## Objetivos de aprendizaje

- Comparar estrategias de planificación para agentes
- Implementar planificación jerárquica y reactiva
- Diseñar orquestación multi-agente (LangChain, CrewAI, Python)
- Gestionar workflows con dependencias y recursos
- Coordinar y resolver conflictos entre agentes

## Orden sugerido

Ver **[0-guia-pedagogica.md](0-guia-pedagogica.md)** para la secuencia por semanas y el mapa de herramientas (LangChain vs CrewAI vs Python puro).

## Contenido por bloque

### Fundamentos y agentes con LLM (requieren `GITHUB_TOKEN` + `GITHUB_BASE_URL` en `.env`)

- [1-basic_planning.py](1-basic_planning.py) — Agente ReAct mínimo con una herramienta (LangChain + hub)
- [1-langchain_planning.py](1-langchain_planning.py) — Agente con herramienta tipo calculadora (LangChain)
- [1-basic-planning-agent.ipynb](1-basic-planning-agent.ipynb) — Notebook de apoyo
- [2-hierarchical-planning.py](2-hierarchical-planning.py) — Planificación jerárquica con LLM
- [2-crewai_orchestration.py](2-crewai_orchestration.py) — Equipo CrewAI
- [5-agent-orchestration.py](5-agent-orchestration.py) — Orquestación con LangChain
- [7-task-decomposition.py](7-task-decomposition.py) — Descomposición de tareas con LLM

### Planificación y workflows (mayormente standalone)

- [1-planning-strategies.py](1-planning-strategies.py) — Comparación de estrategias (Python)
- [2-multiagent_orchestration.py](2-multiagent_orchestration.py) — Coordinación mínima entre dos agentes (Python)
- [3-reactive-planning.py](3-reactive-planning.py) — Planificación reactiva con reglas
- [4-goal-oriented-planning.py](4-goal-oriented-planning.py) — STRIPS / orientada a objetivos
- [6-workflow-management.py](6-workflow-management.py) — DAG, paralelismo y estados de tarea
- [8-resource-allocation.py](8-resource-allocation.py) — Asignación de recursos

### Coordinación avanzada

- [9-multi-agent-coordination.py](9-multi-agent-coordination.py) — Coordinación y mensajes
- [10-conflict-resolution.py](10-conflict-resolution.py) — Resolución de conflictos
- [11-negotiation-strategies.py](11-negotiation-strategies.py) — Negociación
- [12-emergence-behaviors.py](12-emergence-behaviors.py) — Comportamientos emergentes

### Otros

- [Swarm_101.ipynb](Swarm_101.ipynb) — Introducción a enfoques tipo swarm
- [_demo_utils.py](_demo_utils.py) — Utilidades para pausas en demos interactivas

### Lecturas

- [planning-patterns.md](planning-patterns.md)
- [orchestration-guide.md](orchestration-guide.md)
- [coordination-strategies.md](coordination-strategies.md)
- [presentacion.md](presentacion.md)

## Evaluación (referencia)

- Ejercicios prácticos de planificación y orquestación
- Proyecto: sistema multi-agente con flujo no trivial
- Quiz: conceptos de coordinación

## Enlaces útiles

- [LangChain — guía de agentes / tutoriales](https://python.langchain.com/docs/use_cases/autonomous_agents/)
- [CrewAI](https://docs.crewai.com/)
- [Multi-agent systems (Wikipedia)](https://en.wikipedia.org/wiki/Multi-agent_system)
