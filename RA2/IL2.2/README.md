# Módulo IL2.2: Sistemas de Memoria e Integración de Herramientas

Este módulo se centra en dotar a los agentes de IA de **memoria**, una capacidad crucial para pasar de interacciones simples a conversaciones coherentes y contextuales. Exploramos cómo los agentes pueden recordar información pasada para responder preguntas de seguimiento y mantener un diálogo fluido. En la segunda mitad damos el salto al **mundo exterior**: herramientas externas, un registro dinámico de herramientas y el patrón MCP.

## Antes de empezar

- **`GROQ_API_KEY`** en el archivo `.env` (local) o en los **Secrets** de Google Colab.
  Se consigue gratis en [console.groq.com](https://console.groq.com/).
- Modelos que usa cada notebook (están en `.env.example`, no hay que inventarlos):
  - `1-memory-agent` y `2-memory-agent-advanced` → **`GROQ_MODEL`** (`llama-3.3-70b-versatile`).
    Son agentes de LangChain con herramientas, y por esa vía el 70b es el más fiable (6/6 vs 4/6).
  - `3-herramientas-externas` → **`GROQ_MODEL_TOOLS`** (`openai/gpt-oss-20b`), porque encadena
    varias llamadas a herramientas seguidas y ahí los dos Llama fallan (8b 2/4 · gpt-oss 4/4).
- Dependencias: ya vienen en el entorno del repo (`uv sync`). En Colab, la primera celda de
  cada notebook las instala con `pip`.
- **Cuota**: la capa gratuita de Groq limita a 30 peticiones/min y 100K tokens/día en el 70b.
  Si aparece un error `429`, no está roto el código: hay que esperar o cambiar de modelo.

## Contenidos del Módulo

### 1. Agentes con Memoria Conversacional
- **`1-memory-agent.ipynb`**: Introduce el concepto de memoria en los agentes de LangChain. Se implementa un agente que utiliza un historial de chat gestionado manualmente para responder preguntas de seguimiento, demostrando la importancia del contexto en una conversación.

### 2. Sistemas de Memoria Avanzados
- **`2-memory-agent-advanced.ipynb`**: Profundiza en las soluciones de memoria automatizadas que ofrece LangChain para superar las limitaciones de la gestión manual. Se implementan y comparan tres estrategias clave:
  - **`ConversationBufferMemory`**: Para un historial de conversación completo.
  - **`ConversationBufferWindowMemory`**: Para mantener un historial de tamaño fijo, conservando solo las interacciones más recientes.
  - **`ConversationSummaryMemory`**: Para gestionar conversaciones largas resumiendo el historial y ahorrando tokens.

### 3. Herramientas Externas y MCP
- **`3-herramientas-externas.ipynb`**: Del historial interno al mundo exterior. Se define el
  *tool execution loop* completo con el SDK crudo de Groq, un `RegistroHerramientas` dinámico,
  herramientas con estado (carrito, lista de tareas), orquestación multi-paso y una simulación
  de servidor y cliente **MCP**. Cierra con un ejercicio de asistente de productividad.

  **Robustez: el agente que funciona en la demo y se cae con uso real.** La función
  `_pedir_al_modelo` de este notebook no llama al modelo "a pelo": reintenta ante los dos
  fallos normales de un agente en producción, y además desconfía de lo que le devuelve el modelo:

  | Qué falla | Cómo se ve | Cómo se maneja aquí |
  |---|---|---|
  | El modelo genera la llamada a la función mal formada | `400` con el código `tool_use_failed` | Reintento con espera creciente (no es un bug del código: es un fallo probabilístico del modelo) |
  | Se agota la cuota por minuto de la capa gratuita | `429` `rate_limit_exceeded` | Reintento esperando unos segundos |
  | El modelo manda argumentos basura (p. ej. `{"": ""}`) | `TypeError` al invocar la función de Python | Se sanean los argumentos antes de ejecutar nada |

  La idea de fondo: **la salida del LLM es entrada no confiable**. Un agente que no contempla
  estos tres casos parece perfecto en clase y se rompe en cuanto lo usa gente de verdad.

## Conceptos Clave

- **Memoria Conversacional**: La capacidad de un agente para retener y utilizar información de interacciones pasadas.
- **Gestión de Estado (Stateful vs. Stateless)**: La diferencia entre un agente que recuerda el contexto (stateful) y uno que no lo hace (stateless).
- **Estrategias de Memoria**: Diferentes enfoques para gestionar el historial de una conversación, cada uno con sus propias ventajas y casos de uso (Buffer, Window, Summary).
- **Integración de Herramientas (Tool Integration)**: La capacidad de los agentes para utilizar herramientas externas (APIs, bases de datos, etc.) para realizar acciones y obtener información del mundo real.

## Próximos Pasos

Una vez que un agente puede recordar conversaciones y usar herramientas, el siguiente paso es enseñarle a planificar. El **Módulo IL2.3** se centrará en la **planificación y orquestación**, permitiendo a los agentes descomponer objetivos complejos en una serie de pasos ejecutables.