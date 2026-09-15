# Multi-agente en 2026: qué se usa y qué se pide en el mercado

Lectura de clase para **después** de correr `4-langgraph-multiagente.ipynb`.
No reemplaza los algoritmos de Python puro: los sitúa.

## El mapa que un reclutador espera que sepas nombrar

| Pieza | Qué es hoy | En este curso |
|---|---|---|
| **Grafo de agente** | LangGraph (`StateGraph`, `create_agent`, `Command`, `Send`) | IL2.1 + este módulo |
| **Equipo por roles** | CrewAI (`Agent` / `Task` / `Crew`) | `2-crewai_orchestration.py` |
| **Herramientas** | Function calling + **MCP** | IL2.2 |
| **Memoria** | Checkpointer + `thread_id` | RA1 IL1.1 y IL2.2 |
| **Observabilidad** | LangSmith (trazas, eval) | RA3 |
| **Swarm de OpenAI** | Librería **archivada**. El patrón (handoff) vive en LangGraph | `Swarm_101.ipynb` = historia |

No hace falta saber AutoGen, Semantic Kernel o “diez frameworks”. Hace falta **elegir uno y justificar el costo**.

## Tres topologías que se ven en producción

1. **Un agente + herramientas** — el default. Soporte, FAQ, RAG con 2–3 tools.
2. **Supervisor** — un nodo decide la ruta; especialistas no se hablan entre sí. Controlable, fácil de auditar.
3. **Handoff** — un agente **cede el control** a otro (`Command(goto=...)`). Es el recambio del Swarm archivado. Úsalo cuando el siguiente experto necesita el hilo, no solo un resumen.

El **fan-out** (`Send`) es un extra: el mismo nodo en paralelo (revisar 3 cláusulas, 3 CV, 3 chunks). No es “un equipo”: es map-reduce.

## ¿De verdad necesitas multi-agente?

Justifícalo solo si ocurre **una** de estas:

- Los prompts de sistema **chocan** (el auditor no puede ser el vendedor).
- Las herramientas o permisos son **distintos** (el que lee la base no puede escribir el correo).
- Hay trabajo **paralelizable** de verdad (`Send`), no una fila de textos.

Si los “agentes” se pasan un string en línea recta, eso es una **función con pasos**. El mercado castiga el multi-agente decorativo: más tokens, más latencia, más “¿quién falló?”.

## Costos que hay que medir (no intuir)

| Arquitectura | Llamadas típicas / consulta | Qué se rompe primero |
|---|---|---|
| 1 agente + tools | 2–4 | El formato de la tool |
| Supervisor + 1 especialista + síntesis | 3 | El clasificador se equivoca de ruta |
| Handoff A → B → síntesis | 3–5 | Bucle A↔B sin tope |
| Crew de 3 roles secuenciales | 4–8 | Cuota diaria de Groq |
| 5 agentes “que se pongan de acuerdo” | sin tope | La factura |

En la capa gratuita de Groq el límite que se agota primero es **200K tokens/día**. Un Crew “bonito” en la demo puede dejar al curso sin cuota a las 11:00.

**Regla de proyecto:** mide tokens y segundos de **un agente** contra tu equipo. Si el equipo no gana en calidad, no se entrega.

## Recomendación para el proyecto del curso

1. Empieza con `create_agent` + 2 herramientas + checkpointer.
2. Si un rol necesita otro prompt, **un supervisor** (como `3-langgraph-orquestacion.py`).
3. Si el segundo experto debe ver el hilo, **handoff** (`Command`).
4. CrewAI solo si el enunciado pide roles y un `Process` que un grafo de 4 nodos se come.
5. Python puro (DAG, STRIPS, negociación) para la parte que **no** necesita un LLM.
6. Documenta en **IL2.4** (`0-arquitectura-ra2.md`): diagrama del grafo, tope de iteraciones, qué pasa si una tool falla (ya lo viste en IL2.2).

## Lo que se pregunta en entrevistas (y sale en la pauta)

- Diferencia entre **orquestación** (hay un jefe) y **coreografía** (pares). Está en `orchestration-guide.md`.
- Por qué `create_react_agent` de LangGraph y `AgentExecutor` **ya no** son el default.
- Cómo aíslas sesiones (`thread_id`) y cómo evitas que dos agentes se facturen en un bucle.
- MCP: el modelo no “tiene” la tool; habla un contrato.

Si puedes responder eso con el código de este módulo, estás al día con lo que se está contratando para “agentic” en 2026.
