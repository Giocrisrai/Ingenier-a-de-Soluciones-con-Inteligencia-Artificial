# IL1.1 - Introducción a LLMs y Conexiones API

## Introducción

Esta unidad introduce los conceptos fundamentales de los Modelos de Lenguaje Grandes (LLMs) y las técnicas para establecer conexiones API efectivas. Aprenderás a interactuar con diferentes proveedores de LLMs y comprender las bases técnicas para el desarrollo de aplicaciones con IA generativa.

## Videos de cada archivo del curso:

> ⚠️ **Los vídeos se grabaron con el proveedor anterior (GitHub Models).** Las explicaciones
> conceptuales siguen siendo válidas, pero la creación de la cuenta, el nombre de las
> variables de entorno y los nombres de los modelos **ya no coinciden**. Para la parte de
> configuración, sigue siempre este README y los notebooks, no el vídeo.

- **1-groq_model_api.ipynb**: Conexión directa a la API de Groq.
  [![Ver Video](https://img.youtube.com/vi/oYvwSROBTl0/hqdefault.jpg)](https://www.youtube.com/watch?v=oYvwSROBTl0)
- **2-langchain_model_api.ipynb**: Abstracción de la API con LangChain.
  [![Ver Video](https://img.youtube.com/vi/v6Dgw0CMAfs/hqdefault.jpg)](https://www.youtube.com/watch?v=v6Dgw0CMAfs)
- **3-langchain_streaming.ipynb**: Implementación de respuestas en tiempo real (Streaming).
  [![Ver Video](https://img.youtube.com/vi/xENs45V5C3k/hqdefault.jpg)](https://www.youtube.com/watch?v=xENs45V5C3k)
- **4-langchain_memory.ipynb**: Gestión de memoria en conversaciones.
  [![Ver Video](https://img.youtube.com/vi/cM_CJPaD0kQ/hqdefault.jpg)](https://www.youtube.com/watch?v=cM_CJPaD0kQ)


## Antes de empezar: obtén tu API key de Groq

Esta es la **primera** experiencia del curso y todo el material usa [Groq](https://console.groq.com/)
como proveedor de modelos. Necesitas una API key propia (gratuita):

1. Entra a **https://console.groq.com/** y crea una cuenta.
   Se sugiere registrarse con el **correo institucional Duoc UC** (puedes usar "Continue with Google").
2. En el menú lateral abre **API Keys → Create API Key**.
3. Dale un nombre reconocible (por ejemplo `curso-ia-duoc`) y confirma.
4. **Copia la key en ese momento**: empieza por `gsk_...` y solo se muestra una vez.
   Si la pierdes, borra esa key y crea otra (toma 10 segundos).

> **No se requiere tarjeta de crédito.** La capa gratuita de Groq alcanza para todo el curso.

### Límites de la capa gratuita

Los límites vigentes (agosto 2026) se consultan en *Settings → Limits* de la consola y en la
[documentación oficial](https://console.groq.com/docs/rate-limits):

| Modelo | Peticiones/min | Peticiones/día | Tokens/min | **Tokens/día** |
|---|---|---|---|---|
| `openai/gpt-oss-120b` | 30 | 1.000 | 8.000 | **200.000** |
| `openai/gpt-oss-20b` | 30 | 1.000 | 8.000 | **200.000** |

> **El límite que se agota primero es el de tokens al día (TPD).** Ambos gpt-oss tienen
> 200.000 tokens diarios. El modelo rápido (~1000 t/s) conviene para pruebas.

Por eso conviene:
- No ejecutar celdas en bucle sin necesidad.
- Reutilizar respuestas ya obtenidas en lugar de repetir la misma llamada.
- Usar `openai/gpt-oss-20b` mientras pruebas, y dejar `openai/gpt-oss-120b` para la
  ejecución final o las tareas que de verdad necesiten más razonamiento.
- Si aparece un error `429`, **leer el mensaje**: indica qué límite se alcanzó y cuánto esperar.
  Si dice `tokens per minute`, basta con esperar un minuto; si dice `tokens per day`, hay que
  cambiar de modelo o continuar al día siguiente.

### Modelos que usa el curso
| Uso | Modelo |
|---|---|
| Principal (razonamiento, calidad) | `openai/gpt-oss-120b` |
| Rápido (tareas simples, alto volumen) | `openai/gpt-oss-20b` |

## Objetivos de Aprendizaje

Al completar esta unidad, serás capaz de:

1.  **Comprender los fundamentos de los LLMs**: Arquitectura, funcionamiento y capacidades.
2.  **Establecer conexiones API**: Configurar y usar APIs de diferentes proveedores.
3.  **Implementar patrones básicos**: Llamadas síncronas, streaming y gestión de memoria.
4.  **Aplicar mejores prácticas**: Configuración segura, manejo de errores y optimización.

## Contenido del Módulo

Este módulo está compuesto por cuatro cuadernos de Jupyter que te guiarán progresivamente desde una conexión básica hasta la creación de un chatbot con memoria, más un quinto cuaderno de práctica (`practica_1.ipynb`) con ejercicios para resolver por tu cuenta.

### Notebook 1: Conexión Directa con la API de Groq (`1-groq_model_api.ipynb`)
Este cuaderno es el punto de partida. Aprenderás a realizar llamadas directas a un modelo de lenguaje utilizando la API de Groq y su SDK oficial.
- **Qué aprenderás**:
    - Obtener la API key en https://console.groq.com/ y configurarla de forma segura.
    - Configurar la variable de entorno y el cliente de `groq`.
    - Realizar una llamada básica `chat.completions.create`.
    - Usar parámetros clave como `model`, `messages`, `temperature` y `max_tokens`.
    - Aplicar el rol `system` para guiar el comportamiento del modelo.
- **Cómo usarlo**:
    1. Asegúrate de tener la variable de entorno `GROQ_API_KEY` configurada (`.env` en local, Secrets en Colab).
    2. Instala la dependencia `groq`.
    3. Ejecuta las celdas secuencialmente para ver cómo se establece la conexión y se interactúa con el modelo.

### Notebook 2: Abstracción con LangChain (`2-langchain_model_api.ipynb`)
Una vez que entiendes la conexión directa, introducimos LangChain, un framework que simplifica la interacción con LLMs.
- **Qué aprenderás**:
    - Las ventajas de usar un framework como LangChain.
    - Configurar el objeto `ChatGroq` para conectarse al proveedor de modelos.
    - Utilizar el método `invoke` para interactuar con el modelo.
    - Entender la estructura de mensajes de LangChain (`HumanMessage`, `AIMessage`, `SystemMessage`).
- **Cómo usarlo**:
    1. Instala las dependencias `langchain` y `langchain-groq`.
    2. `ChatGroq` lee automáticamente la variable de entorno `GROQ_API_KEY`.
    3. Ejecuta las celdas para comparar la simplicidad del código de LangChain frente a la llamada directa.

### Notebook 3: Streaming en Tiempo Real con LangChain (`3-langchain_streaming.ipynb`)
Este cuaderno se enfoca en mejorar la experiencia de usuario mostrando las respuestas del modelo en tiempo real.
- **Qué aprenderás**:
    - Qué es el streaming y por qué es crucial para aplicaciones interactivas.
    - Implementar streaming usando el método `.stream()` de LangChain.
    - Procesar los "chunks" de datos que llegan en tiempo real.
    - Construir un chatbot simple que responde de forma fluida.
- **Cómo usarlo**:
    1. Ejecuta las celdas para ver la diferencia visual y de percepción entre una respuesta normal (`invoke`) y una con streaming.
    2. Prueba el chatbot interactivo al final del cuaderno para experimentar el streaming en acción.

### Notebook 4: Gestión de Memoria con LangChain (`4-langchain_memory.ipynb`)
Un LLM no tiene estado. Este cuaderno enseña cómo darle "memoria" para que pueda recordar interacciones pasadas.
- **Qué aprenderás**:
    - La importancia de la memoria para conversaciones coherentes.
    - Implementar diferentes estrategias de memoria sobre un checkpointer de LangGraph:
        - Buffer: guarda todo el historial del `thread_id`.
        - Ventana: el modelo solo ve los últimos `k` intercambios.
        - Resumen: compacta mensajes viejos con el propio LLM.
    - Integrar la memoria con `InMemorySaver` + `thread_id`
      (sustituye a `RunnableWithMessageHistory`, deprecado en LangChain 1.x).
- **Cómo usarlo**:
    1. Ejecuta los ejemplos de cada tipo de memoria para entender sus ventajas y desventajas.
    2. Analiza la comparación final para ver cómo cada tipo de memoria responde a la misma secuencia de preguntas.
    3. Experimenta con el chatbot de memoria configurable para cambiar de estrategia en tiempo real.

### Práctica: Exploración de LLMs con API y LangChain (`practica_1.ipynb`)
Cuaderno de ejercicios para consolidar lo visto en los cuatro notebooks anteriores: comparación de
modelos de Groq, efecto de la `temperature`, mensajes de sistema, streaming con el SDK directo y un
chatbot con memoria construido a mano. Se resuelve después de completar los notebooks 1 a 4.

## Configuración del Entorno

### Variables de Entorno Requeridas

Copia `.env.example` a `.env` en la raíz del repositorio y completa:

```bash
GROQ_API_KEY="gsk_tu_api_key_aqui"
GROQ_MODEL="openai/gpt-oss-120b"
GROQ_MODEL_FAST="openai/gpt-oss-20b"
```

En Google Colab, en lugar del `.env`, crea el secreto `GROQ_API_KEY` en el panel 🔑 **Secrets**.

### Dependencias

```bash
pip install groq langchain langchain-groq python-dotenv
```

## Arquitectura Técnica

### Carga de credenciales (Colab y local)

```python
import os

try:
    from google.colab import userdata  # type: ignore
    os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()

MODELO = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
```

### Patrón de Conexión API

```python
# Configuración estándar con el SDK oficial de Groq
from groq import Groq

cliente = Groq()  # lee GROQ_API_KEY del entorno
```

### Abstracción con LangChain

```python
# Framework approach
from langchain_groq import ChatGroq

llm = ChatGroq(
    model=MODELO,
    temperature=0.2
)
```

## Consideraciones Técnicas

### Seguridad
- Nunca hardcodear API keys en el código
- Usar variables de entorno para credenciales (`.env` está en `.gitignore`)
- Implementar rate limiting y error handling (la capa gratuita devuelve `429` al excederse)

### Performance
- Configurar timeouts apropiados
- Usar streaming para respuestas largas
- Optimizar el uso de tokens

### Escalabilidad
- Considerar patrones de retry y circuit breaker
- Implementar logging para debugging
- Planificar para múltiples proveedores

## Evaluación

Esta unidad incluye:
- **Quiz teórico** (8 preguntas) sobre fundamentos de LLMs
- **Práctica dirigida** con los notebooks proporcionados
- **Ejercicios de implementación** para reforzar conceptos

## Recursos Adicionales

- [Consola de Groq](https://console.groq.com/) (API Keys, Playground y límites)
- [Documentación de la API de Groq](https://console.groq.com/docs/overview)
- [Catálogo de modelos en Groq](https://console.groq.com/docs/models)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Transformer Architecture Paper](https://arxiv.org/abs/1706.03762)

## Próximos Pasos

Al completar IL1.1, estarás preparado para:
- **IL1.2**: Técnicas avanzadas de prompt engineering
- **IL1.3**: Implementación de sistemas RAG
- **IL1.4**: Evaluación y optimización de LLMs