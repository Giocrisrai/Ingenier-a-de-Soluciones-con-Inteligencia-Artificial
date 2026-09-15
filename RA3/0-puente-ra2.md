# De RA2 a RA3: qué se observa

RA3 no inventa otro agente. Observa, audita y endurece **el grafo que ya
construiste** (`create_agent` / `StateGraph`, tools, `thread_id`).

| En RA2 lo llamaste | En RA3 lo mides |
|---|---|
| Una consulta | `trace_id` (una petición) |
| `thread_id` (IL2.2) | Misma conversación a lo largo de varias trazas |
| Nodo `model` / `tools` / supervisor | Span o etapa del log |
| `Command(goto=...)` / `Send` | Salto de ruta (quién habló, cuántas veces) |
| Tool (`@tool`, MCP) | Latencia + error `400 tool_use_failed` / `429` |
| ADR de runtime (IL2.4) | Qué aparece en LangSmith y qué no |

```text
Usuario  →  grafo LangGraph  →  Groq
                │
                ├── logs JSON (este módulo, a mano)
                ├── métricas (latencia, tokens, costo)
                └── LangSmith (si LANGSMITH_TRACING=true)
```

## Orden

1. **IL3.1** — métricas y logs sobre una llamada (SDK crudo a propósito: ves el costo).
   Opcional: `IL3.1/3-observar-grafo.py` aplica lo mismo a `create_agent`.
2. **IL3.2** — una traza = árbol de etapas. En el grafo, cada nodo es un span.
3. **IL3.3** — injection, mínimo privilegio de tools, memoria envenenada (`thread_id`).
4. **IL3.4** — tokens/día (200K en Groq free), `GROQ_MODEL_FAST`, no añadir nodos sin medir.
5. **IL3.5** — el mismo `.env` (`GROQ_*`, `LANGSMITH_*`) en AWS.

`AgentExecutor` no se observa: es contraste de IL2.1, no el runtime del proyecto.
