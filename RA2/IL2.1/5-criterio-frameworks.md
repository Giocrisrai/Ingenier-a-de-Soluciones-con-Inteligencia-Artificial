# Criterio: qué runtime usar (y cuándo no)

No hay un ganador absoluto. El ejercicio de IL2.1 es **correr el mismo tipo de problema** en cuatro sitios y anotar evidencia, no memorizar una API.

| Camino | Archivo | Qué orquesta | Qué ves al depurar |
|---|---|---|---|
| A mano | `1-agent-fundamentals.ipynb` | Tu `if/else` | El texto crudo del modelo |
| Function calling | `2-agent-function-calling.ipynb` | Tu loop + JSON de Groq | `tool_calls` estructurados |
| LangGraph (actual) | `3-langgraph-agent.ipynb` | Un `StateGraph` | Nodos, aristas, `thread_id` |
| Clásico | `3-langchain-agent.ipynb` | `AgentExecutor` | La caja `Entering new AgentExecutor chain` |
| Equipo por roles | `4-crewai-agent.ipynb` | `Crew` + `Process` | Roles, tasks, handoff |

## Después de ejecutar 3, 3-clásico y 4

Llena esto en clase (una frase por celda basta):

| Pregunta | LangGraph | AgentExecutor | CrewAI |
|---|---|---|---|
| ¿Cuántas líneas hasta la primera respuesta útil? | | | |
| ¿Dónde se rompe si Wikipedia falla? | | | |
| ¿Puedo dibujar el flujo en la pizarra? | | | |
| ¿Cuántas llamadas al LLM hizo Marie Curie? | | | |
| ¿Lo usaría en un repo nuevo esta semana? | | | |

## Reglas que sí se llevan a producción

1. **Un agente basta** si el trabajo es un loop de herramientas. CrewAI no es "más profesional": es más caro y más difícil de depurar.
2. **Grafo a mano** cuando la topología no es ReAct (rutas, human-in-the-loop, dos especialistas con un supervisor).
3. **`create_agent`** cuando quieres el ReAct vigente sin armar el grafo. Es el default de LangChain 1.x.
4. **`AgentExecutor`** para *leer* código de 2023-2025, no para empezarlo.
5. **CrewAI** cuando hay roles con prompts incompatibles y un proceso (secuencial/jerárquico) que un grafo de 4 nodos se come.
6. Mide **tokens y segundos por tarea completa**. Si el equipo no gana en calidad, no compensa.

## Puente a IL2.2, IL2.3 e IL2.4

- Memoria: el `thread_id` de RA1 es el mismo objeto, ahora con herramientas.
- Planificación y multi-agente: `3-langgraph-planning.py`, `4-langgraph-multiagente.ipynb` y `4-tendencias-multiagente.md`. El Python puro de IL2.3 no se toca: ahí se aprende el algoritmo.
- Documentación: `IL2.4/0-arquitectura-ra2.md` — el ADR de runtime es esta misma tabla, justificada con tokens.
