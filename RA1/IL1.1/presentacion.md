# Presentación IL1.1 - Introducción a LLMs y Conexiones API

## Slide 1: Título y Objetivos
**Título:** IL1.1 - Introducción a LLMs y Conexiones API  
**Subtítulo:** Fundamentos de Modelos de Lenguaje Grandes

**Objetivos:**
- Comprender los fundamentos de los LLMs
- Establecer conexiones API con diferentes proveedores
- Implementar patrones básicos de uso
- Aplicar mejores prácticas de seguridad

---

## Slide 2: ¿Qué son los LLMs?
**Título:** Fundamentos de los Modelos de Lenguaje Grandes

**Contenido:**
- **Arquitectura:** Basados en Transformers
- **Funcionamiento:** Predicción de tokens basada en contexto
- **Capacidades:** Generación, comprensión y análisis de texto
- **Proveedores principales:** Groq, OpenAI, Anthropic, Google
- **Proveedor del curso:** Groq (https://console.groq.com/) con modelos Llama

**Conceptos clave:**
- Tokens, embeddings, atención
- Entrenamiento y fine-tuning

---

## Slide 3: Configuración del Entorno
**Título:** Preparación Técnica

**Paso 0 - Obtener la API key (gratis, sin tarjeta de crédito):**
1. Entrar a https://console.groq.com/ y crear cuenta (se sugiere correo Duoc UC)
2. Menú lateral: **API Keys → Create API Key**
3. Copiar la key `gsk_...` (solo se muestra una vez)

**Variables de entorno requeridas (`.env`):**
```bash
GROQ_API_KEY="gsk_tu_api_key_aqui"
GROQ_MODEL="openai/gpt-oss-120b"
GROQ_MODEL_FAST="openai/gpt-oss-20b"
```
En Google Colab: panel 🔑 **Secrets** con el secreto `GROQ_API_KEY`.

**Dependencias:**
```bash
pip install groq langchain langchain-groq python-dotenv
```

**Mejores prácticas de seguridad:**
- Nunca hardcodear API keys
- Usar variables de entorno (o Secrets de Colab)
- Respetar el free tier: 30 req/min, 8.000 tokens/min y **200.000 tokens/día**
  (error `429` si se excede). Ambos gpt-oss comparten ese tope diario.

---

## Slide 4: Conexión Directa con API
**Título:** Notebook 1 - Groq API (`1-groq_model_api.ipynb`)

**Pasos a seguir:**
1. Crear la cuenta en Groq y generar la API key
2. Configurar el cliente oficial `groq`
3. Realizar primera llamada básica al modelo
4. Explorar parámetros: temperature, max_tokens
5. Implementar manejo de errores
6. Usar mensajes de sistema para definir comportamiento

**Código básico:**
```python
from groq import Groq

cliente = Groq()  # lee GROQ_API_KEY del entorno
```

---

## Slide 5: Framework LangChain
**Título:** Notebook 2 - LangChain Model API

**Ventajas de LangChain:**
- Interfaz unificada para múltiples proveedores
- Abstracción de complejidad
- Herramientas adicionales integradas
- Mejor para prototipado rápido

**Implementación:**
```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    temperature=0.2
)
```

**Tipos de mensajes:** HumanMessage, AIMessage, SystemMessage

---

## Slide 6: Streaming en Tiempo Real
**Título:** Notebook 3 - LangChain Streaming

**¿Qué es el streaming?**
- Recibir respuesta token por token
- Mejora percepción de velocidad
- Interfaces más reactivas

**Cuándo usar streaming:**
- Respuestas largas (>100 tokens)
- Chatbots y asistentes
- Aplicaciones interactivas
- Demostraciones en vivo

**Implementación:**
```python
for chunk in llm.stream([HumanMessage(content=prompt)]):
    print(chunk.content, end="", flush=True)
```

---

## Slide 7: Gestión de Memoria
**Título:** Notebook 4 - Memoria conversacional con LangGraph

`RunnableWithMessageHistory` está deprecado. La memoria de hilo usa un **checkpointer** (`InMemorySaver`) y un **`thread_id`**.

**Estrategias:**
- **Buffer:** el modelo ve todo el historial
- **Ventana:** solo los N intercambios más recientes
- **Resumen:** compacta el pasado para ahorrar tokens

**Cuándo usar cada tipo:**
- Buffer: Conversaciones cortas e importantes
- Window: Contexto reciente limitado
- Summary: Sesiones largas con optimización de tokens

---

## Slide 12: Casos de Uso Prácticos
**Título:** Aplicaciones Comunes

**Análisis de texto:**
- Extracción de temas principales
- Análisis de sentimiento
- Identificación de palabras clave

**Generación de contenido:**
- Artículos y documentación
- Respuestas personalizadas
- Creatividad dirigida

**Asistentes conversacionales:**
- Chatbots con memoria
- Soporte técnico automatizado
- Interfaces de usuario naturales

---

## Slide 13: Evaluación del Módulo
**Título:** Componentes de Evaluación

**Quiz teórico (8 preguntas):**
- Fundamentos de LLMs
- Conceptos de tokens y arquitectura
- Mejores prácticas de seguridad
- Comparación de enfoques

**Práctica dirigida:**
- Ejecución de los 4 notebooks
- Experimentación con parámetros
- Implementación de casos de uso

**Ejercicios adicionales:**
- Crear asistente especializado
- Optimización de tokens
- Chatbot con memoria

---

## Slide 14: Recursos y Próximos Pasos
**Título:** Continuando el Aprendizaje

**Recursos adicionales:**
- [Consola de Groq](https://console.groq.com/) (API Keys, Playground y límites)
- [Documentación de la API de Groq](https://console.groq.com/docs/overview)
- [Catálogo de modelos en Groq](https://console.groq.com/docs/models)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Transformer Architecture Paper](https://arxiv.org/abs/1706.03762)

**Próximos módulos:**
- **IL1.2:** Técnicas avanzadas de prompt engineering
- **IL1.3:** Implementación de sistemas RAG
- **IL1.4:** Evaluación y optimización de LLMs

---