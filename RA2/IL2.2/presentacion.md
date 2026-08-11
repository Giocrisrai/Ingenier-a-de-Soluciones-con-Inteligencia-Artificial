# IL2.2: Sistemas de Memoria e Integración de Herramientas

## Objetivos de la Sesión
- Comprender la importancia de la memoria para la persistencia en agentes conversacionales.
- Implementar y comparar diferentes estrategias de memoria en LangChain.
- Automatizar la gestión del historial de chat para crear agentes robustos.
- Explorar el protocolo de contexto de modelo (MCP) para la integración avanzada de herramientas.
- Preparar la transición hacia la planificación y orquestación de tareas complejas.

## 1. La Necesidad de un Agente con Estado (Stateful)

Hasta ahora, nuestros agentes han sido **sin estado (stateless)**. Cada interacción es independiente, lo que impide conversaciones fluidas y la realización de tareas que requieren contexto. Un agente verdaderamente útil debe recordar interacciones pasadas para:
- Responder preguntas de seguimiento.
- Mantener el hilo de la conversación.
- Acumular información a lo largo del tiempo.
- Personalizar la experiencia del usuario.

La **memoria** es el componente que transforma un agente reactivo en un asistente conversacional coherente.

## 2. Gestión de Memoria en LangChain

LangChain ofrece un potente conjunto de abstracciones para gestionar la memoria, evitando la gestión manual y los problemas de escalabilidad.

### Del Historial Manual a los Sistemas Automatizados

- **Gestión Manual**:
  - **Implementación**: Se mantiene una lista de `HumanMessage` y `AIMessage` que se pasa explícitamente en cada llamada al `AgentExecutor`.
  - **Ventajas**: Simple de entender y bueno para depuración.
  - **Limitaciones**: Propenso a errores, repetitivo y no gestiona el tamaño del contexto.

- **Sistemas de Memoria de LangChain**:
  - **Abstracción Clave**: Clases de memoria que se conectan al agente y gestionan el historial automáticamente.
  - **Ventajas**: Código más limpio, robusto y estrategias integradas para gestionar la longitud del contexto.

### Estrategias de Memoria Implementadas:

1.  **`ConversationBufferMemory`**:
    - **Descripción**: Almacena la conversación completa en un búfer. Es el equivalente automatizado de la gestión manual.
    - **Caso de Uso**: Ideal para conversaciones cortas donde cada detalle es crucial.

2.  **`ConversationBufferWindowMemory`**:
    - **Descripción**: Mantiene una "ventana" de las últimas `k` interacciones. Descarta los mensajes más antiguos para mantener el contexto relevante y dentro de los límites.
    - **Caso de Uso**: Chatbots de servicio al cliente, donde el contexto reciente es lo más importante.

3.  **`ConversationSummaryMemory`**:
    - **Descripción**: Utiliza un LLM para crear y actualizar un resumen de la conversación. En lugar de pasar el historial completo, solo se pasa el resumen.
    - **Caso de Uso**: Conversaciones muy largas, asistentes de investigación o cualquier escenario donde el contexto general es más importante que los detalles literales.

### Comparativa de Estrategias:

| **Estrategia** | **Ventajas** | **Desventajas** | **Mejor Para** |
|---|---|---|---|
| **Buffer** | Retención total de la información | Excede rápidamente el límite de tokens | Conversaciones cortas y de alta fidelidad |
| **Window** | Control predecible del contexto | Pierde información antigua | Mantener relevancia en el corto plazo |
| **Summary** | Escalable a conversaciones infinitas | Consume tokens para resumir, puede perder detalles | Asistentes a largo plazo y análisis de temas |

## 3. Integración de Herramientas y el Protocolo de Contexto de Modelo (MCP)

Mientras que la memoria gestiona el **historial interno**, la verdadera potencia de un agente reside en su capacidad para interactuar con el **mundo exterior** a través de herramientas.

- **Tool Integration**:
  - En IL2.1, integramos herramientas simples como Wikipedia.
  - Un agente avanzado necesita acceder a APIs, bases de datos, sistemas de archivos y otros servicios.

- **Model Context Protocol (MCP)**:
  - Es un estándar emergente que busca unificar cómo los modelos acceden a herramientas externas.
  - **Objetivo**: Crear un "lenguaje universal" para que cualquier modelo pueda usar cualquier herramienta sin adaptaciones complejas.
  - **Concepto Clave**: Define un esquema (`schema`) claro sobre qué puede hacer una herramienta y qué información necesita, similar a como OpenAPI/Swagger documenta las APIs.

Aunque aún no es un estándar universalmente adoptado, los principios de MCP (descripciones claras, esquemas de entrada/salida) son fundamentales para construir agentes robustos y extensibles.

## 4. Robustez: los fallos que sí van a ocurrir

Un agente con herramientas no falla solo cuando falla la herramienta. Falla porque **la salida
del LLM es entrada no confiable**. En `3-herramientas-externas.ipynb` esto no se cuenta, se
implementa: la función que llama al modelo contempla tres casos:

| Qué falla | Cómo se ve | Cómo se maneja |
|---|---|---|
| El modelo genera la llamada a la función mal formada | `400` `tool_use_failed` | Reintento con espera creciente |
| Se agota la cuota por minuto de la capa gratuita | `429` `rate_limit_exceeded` | Reintento esperando unos segundos |
| El modelo manda argumentos basura (p. ej. `{"": ""}`) | `TypeError` al invocar la función Python | Sanear los argumentos antes de ejecutar |

**Por qué importa en clase:** ninguno de los tres es un bug del código del alumno. Los tres son
comportamiento normal de un modelo probabilístico contra una API con cuota. Un agente que no los
contempla funciona en la demo y se cae con uso real.

## 5. Implementaciones y Próximos Pasos

### Implementaciones del Módulo:
1.  **Agente con Memoria Manual**: Se muestra cómo un agente puede recordar el contexto pasando manualmente el `chat_history`.
2.  **Agente con Memoria Automatizada**: Se refactoriza el código para usar `ConversationBufferMemory`, `ConversationBufferWindowMemory` y `ConversationSummaryMemory`, demostrando las ventajas de cada una.
3.  **Agente con Herramientas Externas y MCP**: Tool execution loop con el SDK de Groq, registro dinámico de herramientas, herramientas con estado, orquestación multi-paso y una simulación de servidor/cliente MCP.

### Preparación para IL2.3:
Con un agente que puede **recordar** (memoria) e **interactuar** (herramientas), el siguiente paso lógico es enseñarle a **planificar**.

- **Desafío**: ¿Cómo aborda un agente un objetivo complejo como "organiza mis vacaciones a Tokio"? Esto requiere múltiples pasos: buscar vuelos, encontrar hoteles, sugerir actividades, etc.
- **Solución**: La **planificación** permite al agente descomponer un objetivo grande en una secuencia de tareas más pequeñas y ejecutarlas en orden.

Este módulo sobre memoria y herramientas sienta las bases para el **Módulo IL2.3: Planificación y Orquestación de Agentes**, donde pasaremos de agentes que responden a agentes que **logran objetivos**.
