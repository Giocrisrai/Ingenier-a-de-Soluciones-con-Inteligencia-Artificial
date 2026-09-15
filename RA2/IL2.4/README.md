# IL2.4: Documentacion Tecnica y Diseno de Arquitectura

## Descripcion

Cierra RA2: documentar el sistema de agentes que ya construiste (LangGraph,
memoria con `thread_id`, tools/MCP, supervisor / handoff / `Send`) y dejar
una arquitectura que RA3 pueda observar. No es un modulo de "agentes
genericos": el vocabulario es el de IL2.1–IL2.3.

## Objetivos de Aprendizaje

- Mapear capas (presentacion / aplicacion / dominio / infraestructura) a un grafo LangGraph
- Escribir un ADR corto de runtime (`create_agent` vs `StateGraph` vs CrewAI vs clasico)
- Documentar contratos: estado, tools, `thread_id`, tope de iteraciones, tokens
- Aplicar configuracion por entorno, validacion, reintentos y errores como resultado

## Archivos del Modulo

| Archivo | Descripcion |
|---------|-------------|
| [0-arquitectura-ra2.md](0-arquitectura-ra2.md) | Plantilla del entregable: ADR, vista C4, contratos, checklist. Empieza por aqui. |
| [1-architecture_example.py](1-architecture_example.py) | Arquitectura en capas. `AgenteOrquestador` es un supervisor **sin LLM** (clasifica → tool). Incluye autotest. |
| [2-best_practices.py](2-best_practices.py) | Config desde entorno, validacion, backoff, `ResultadoOperacion`. API simulada (no gasta Groq). |
| [presentacion.md](presentacion.md) | Slides: capas, grafo RA2, testing, deploy, puente a RA3. |

## Antes de empezar

Los dos scripts son **autocontenidos**: no llaman a ningun LLM, no necesitan
`GROQ_API_KEY` ni internet.

```bash
uv run python RA2/IL2.4/1-architecture_example.py
uv run python RA2/IL2.4/2-best_practices.py
```

`2-best_practices.py` simula la API (fallos aleatorios) para ver el backoff
sin cuota. Los nombres `API_KEY` / `MODELO_LLM` son didacticos; si ya tienes
`.env` del curso, el script lee `GROQ_MODEL_FAST` / `GROQ_MODEL` como fallback.

## Como se conecta con el resto de RA2

| Ya lo hiciste | Aqui lo documentas |
|---|---|
| IL2.1 `create_agent` / grafo / CrewAI / clasico | ADR: por que eliges uno |
| IL2.2 checkpointer + `thread_id` + MCP | Contrato de memoria y de tools |
| IL2.3 supervisor, `Command`, `Send`, Python puro | Diagrama de nodos y costo en tokens |

Siguiente: **RA3**. Mapa en [`RA3/0-puente-ra2.md`](../../RA3/0-puente-ra2.md).
LangSmith observa *este* grafo, no un `AgentExecutor`.

## Material de Presentacion

[presentacion.md](presentacion.md)
