# Presentación IL1.3 - Infraestructura RAG

## Slide 1: Título y Objetivos
**Título:** IL1.3 - Infraestructura RAG (Retrieval-Augmented Generation)
**Subtítulo:** Conectando LLMs con Conocimiento Externo y Verificable

**Objetivos:**
- Comprender la arquitectura RAG y sus componentes.
- Implementar el flujo completo: Carga, División, Embeddings y Generación.
- Utilizar bases de datos vectoriales para una recuperación de información eficiente.
- Aplicar RAG para mejorar la precisión y fiabilidad de los LLMs.

---

## Slide 2: ¿Qué es RAG y Por Qué es Crucial?
**Título:** El Framework de Recuperación Aumentada

**Contenido:**
- **Definición:** Una arquitectura que combina un recuperador de información con un generador (LLM) para producir respuestas basadas en un corpus de conocimiento externo.
- **Proceso:**
    1.  **Recuperar:** Busca fragmentos de información relevante para la consulta del usuario.
    2.  **Aumentar:** Inserta esos fragmentos como contexto en el prompt del LLM.
    3.  **Generar:** El LLM sintetiza una respuesta a partir del contexto proporcionado.
- **Beneficios:** Reduce alucinaciones, permite el uso de datos actualizados y privados, y aumenta la transparencia al poder citar fuentes.

---

## Slide 3: Notebooks 1 & 2 - Fundamentos y Preparación de Datos
**Título:** Del Documento a los Fragmentos (`Chunks`)

**Notebook `1-basic-rag.ipynb`:**
- Se introduce el concepto de RAG con un ejemplo mínimo y funcional.
- Se muestra el flujo completo de manera simplificada para entender la interacción entre el recuperador y el generador.

**Notebook `2-text-chunking.py`:**
- Se explora la importancia de la **división de texto** (`Text Splitting`).
- Se analizan diferentes estrategias (ej. `RecursiveCharacterTextSplitter`) y el impacto del tamaño y solapamiento (`chunk_size`, `chunk_overlap`) en la calidad de la recuperación.

---

## Slide 4: Notebooks 3 & 4 - Embeddings y Búsqueda Vectorial
**Título:** De Fragmentos a Respuestas Inteligentes

**Notebook `3-embeddings-simple-rag.ipynb`:**
- Se explica cómo los **modelos de embeddings** convierten los `chunks` de texto en vectores numéricos que capturan su significado semántico.
- Se implementa una búsqueda de similitud simple para encontrar los `chunks` más relevantes.

**Notebook `4-vector-rag.ipynb`:**
- Se introduce el concepto de **Base de Datos Vectorial** (`Vector Store`).
- Se utiliza una base de datos como FAISS o Chroma para almacenar los embeddings de forma eficiente y realizar búsquedas a gran escala, creando un sistema RAG más robusto.

---

## Slide 4b: ¿Por qué los embeddings NO los calcula Groq?
**Título:** Un RAG con dos proveedores

**El problema:**
- Usamos **Groq** (`llama-3.3-70b-versatile`) para la generación, pero **Groq no expone un endpoint de embeddings**: su API solo ofrece chat/completions.
- Un RAG necesita vectores sí o sí, así que hay que resolverlos por otra vía.

**La solución del curso: embeddings locales**
- Modelo `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` vía `langchain-huggingface`, ejecutado **en la máquina del alumno**.

| Pieza | Dónde corre | Coste |
|---|---|---|
| Generación (chat) | API de Groq | API key gratuita |
| Embeddings | Local (HuggingFace) | gratis, sin API key |

**Por qué esto es buena ingeniería, no un parche:**
- **Coste cero por token** al indexar corpus grandes.
- **Privacidad**: los documentos nunca salen de la máquina.
- **Sin conexión** una vez descargado el modelo.

**Lo que hay que advertir a los alumnos:**
- La **primera ejecución descarga ~470 MB** del modelo (luego queda en caché).
- Los vectores pasan de 1536 a **384 dimensiones**: menos memoria y búsqueda más rápida, algo menos de precisión.
- La interfaz de LangChain (`embed_documents` / `embed_query`) es la misma, por lo que **FAISS y el resto del pipeline no cambian**.

---

## Slide 5: Evaluación del Módulo
**Título:** Componentes de Evaluación

**Quiz teórico:**
- Preguntas sobre la arquitectura RAG, sus componentes (Retriever, Vector Store) y sus beneficios (reducción de alucinaciones).

**Práctica dirigida:**
- Ejecución de los 4 notebooks, desde el RAG básico hasta la implementación con base de datos vectorial.
- Experimentación con diferentes estrategias de `chunking` y su impacto en las respuestas.

**Ejercicios adicionales:**
- Aplicar el sistema RAG a un nuevo documento PDF o de texto.
- Intercambiar el modelo de embeddings (por ejemplo `all-mpnet-base-v2`, de 768 dimensiones) y observar los cambios en la calidad de la recuperación y en el tiempo de indexación.
- Comparar la latencia de generación entre `llama-3.3-70b-versatile` y `llama-3.1-8b-instant` en Groq.

---

## Slide 6: Recursos y Próximos Pasos
**Título:** Continuando el Aprendizaje

**Recursos adicionales:**
- [Consola de Groq (crear API key gratuita)](https://console.groq.com/)
- [Modelos de sentence-transformers en HuggingFace](https://huggingface.co/sentence-transformers)
- [LangChain RAG Documentation](https://python.langchain.com/docs/use_cases/question_answering/)
- [Blog de Pinecone: ¿Qué es RAG?](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [FAISS: A library for efficient similarity search](https://engineering.fb.com/2017/03/29/faiss-a-library-for-efficient-similarity-search/)

**Próximos módulos:**
- **IL1.4: Evaluación y Optimización de LLMs:** Aprenderemos a medir cuantitativamente el rendimiento de nuestro sistema RAG para poder mejorarlo.