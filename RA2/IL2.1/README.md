# IL2.1: Arquitectura y Frameworks de Agentes

## 📋 Descripción General

En este módulo exploramos los fundamentos de la arquitectura de agentes inteligentes basados en LLM, progresando desde implementaciones básicas hasta frameworks avanzados como LangChain y CrewAI. Incluye configuraciones específicas para integración con la API de Groq y soluciones a problemas comunes de compatibilidad.

## 🎯 Objetivos de Aprendizaje

- Comprender qué es un agente inteligente y sus componentes fundamentales (cerebro, memoria, herramientas, planificación)
- Dominar el ciclo de razonamiento ReAct (Reason + Act) y el Function Calling (tool calling) nativo de Groq
- Implementar agentes desde cero y usando frameworks LangChain y CrewAI
- Configurar correctamente frameworks con la API de Groq
- Diseñar equipos de agentes colaborativos para tareas complejas
- Entender criterios de selección entre diferentes frameworks

## 📚 Contenido del Módulo

### 1. Fundamentos de Agentes Inteligentes
- **[1-agent-fundamentals.ipynb](1-agent-fundamentals.ipynb)** - Implementación de agente básico desde cero
  - Conceptos fundamentales: cerebro, memoria, herramientas
  - Ciclo ReAct (Reason + Act) manual
  - Parsing de texto y gestión de estado
  - Limitaciones y motivación para frameworks

### 2. Function Calling Nativo
- **[2-agent-function-calling.ipynb](2-agent-function-calling.ipynb)** - Mecanismo estructurado de tool calling
  - Definición de herramientas con JSON Schema
  - Ventajas sobre parsing manual: confiabilidad, seguridad
  - Flujo de llamadas estructuradas
  - Integración con Wikipedia API

### 3. Framework LangChain
- **[3-langchain-agent.ipynb](3-langchain-agent.ipynb)** - Agentes individuales potentes
  - Abstracciones de alto nivel: AgentExecutor, Tool
  - Configuración simplificada con decoradores
  - Gestión automática de historial y errores
  - Tipos de agentes: Zero-shot, Conversational, Structured

### 4. Framework CrewAI
- **[4-crewai-agent.ipynb](4-crewai-agent.ipynb)** - Equipos colaborativos de agentes
  - Conceptos: Agent, Task, Crew, Process
  - Especialización por roles: Investigador, Escritor
  - Coordinación secuencial con dependencias
  - **🔧 CONFIGURACIÓN CRÍTICA**: Prefijo `groq/` en el modelo (CrewAI usa LiteLLM)

## 🔧 Configuraciones Técnicas Importantes

### Variables de Entorno Requeridas
```bash
export GROQ_API_KEY="gsk_tu_api_key_de_groq"
export GROQ_MODEL="openai/gpt-oss-120b"
export GROQ_MODEL_FAST="openai/gpt-oss-20b"
export GROQ_MODEL_TOOLS="openai/gpt-oss-20b"
```

Consigue tu API key gratuita en [console.groq.com](https://console.groq.com/).

> **Cuota de la capa gratuita.** Ambos gpt-oss: 30 peticiones/min, 1.000/día,
> 8K tokens/min y **200K tokens/día**. El límite que se agota primero es el diario de tokens.
> Si aparece un error **`429`**, no está roto el código: hay que esperar o cambiar de modelo
> (`GROQ_MODEL=openai/gpt-oss-20b`).

### ⚠️ Qué modelo usar según el tipo de agente

El *tool calling* no lo resuelve la API por su cuenta: es el **modelo** el que debe generar la
llamada a la función con el formato exacto que la API espera. Si se equivoca, Groq responde
con un error `400` y el código `tool_use_failed`.

Lo medimos con las herramientas de estos mismos notebooks, y el resultado es menos intuitivo
de lo que parece:

| Vía de código | `openai/gpt-oss-120b` | `openai/gpt-oss-20b` |
|---|---|---|
| SDK crudo de Groq, esquema JSON escrito a mano, prompt en español | 7/10 | **10/10** |
| LangChain `create_openai_tools_agent` con el prompt `hwchase17/openai-tools-agent` (en inglés) | **6/6** | 4/6 |

**El "mejor modelo para herramientas" se invierte según la vía.** No hay un ganador absoluto:
depende del prompt del sistema y de cómo se le presenten las herramientas al modelo.

Y hay un tercer caso: cuando el agente encadena **varias** llamadas a herramientas dentro de una
misma conversación, **los dos Llama fallan**. Medido con una cadena de 2 pasos, 4 intentos:
`llama-3.1-8b` 2/4 · `openai/gpt-oss-20b` **4/4**. Por eso existe `GROQ_MODEL_TOOLS`
(`openai/gpt-oss-20b`, un modelo open-weight servido por Groq, no la API de OpenAI).

Por eso en este curso:

- **Herramientas con el SDK crudo, una llamada por consulta** → `GROQ_MODEL_FAST`
  (`openai/gpt-oss-20b`). Notebook `2-agent-function-calling`.
- **Cadenas multi-paso de herramientas** → `GROQ_MODEL_TOOLS` (`openai/gpt-oss-20b`).
  Notebook `3-herramientas-externas` de IL2.2.
- **Agentes de LangChain con herramientas** → `GROQ_MODEL` (`openai/gpt-oss-120b`).
  Notebooks `3-langchain-agent` y, en IL2.2, `1-memory-agent` y `2-memory-agent-advanced`.
- **Agentes ReAct por prompt** (`create_react_agent`) → `GROQ_MODEL`. No les afecta, porque el
  modelo escribe texto plano en vez de una llamada estructurada.

### El mismo test, en otro proveedor

Repetimos exactamente la misma medición contra **Mistral**, que habla el mismo protocolo
(lo viste en IL1.1) y también tiene capa gratuita:

| Modelo | Llamadas correctas (10 intentos) | Cadenas multi-paso (4 intentos) |
|---|---|---|
| `openai/gpt-oss-120b` (Groq) | 7/10 | falla |
| `openai/gpt-oss-20b` (Groq) | 10/10 | 2/4 |
| `mistral-small-latest` | **10/10** | **4/4** |

Mistral acierta donde los Llama fallan, incluidas las cadenas de varios pasos que en este
curso obligaron a añadir reintentos. **Eso no significa que Mistral sea "mejor"**: significa
que el formato de llamada a herramientas se le da mejor. Otro modelo puede ganarle en
razonamiento, en velocidad o en coste.

La conclusión práctica no es "usa Mistral", sino: **cuando montes un agente, mide el
proveedor y el modelo con TUS herramientas antes de decidir.** Es barato de medir y caro
de descubrir en producción.

Dos lecciones que se llevan a producción:

1. **El modelo más grande no es automáticamente el mejor para un agente.** Cuando el agente
   depende de un formato de salida exacto, la fiabilidad de ese formato pesa tanto como la
   capacidad de razonamiento.
2. **Hay que medirlo, no suponerlo**, y medirlo con *tu* prompt y *tus* herramientas: cambiar
   el prompt del sistema fue suficiente para invertir qué modelo era el más fiable.

Y en cualquier caso, trata `tool_use_failed` como un error **esperable**: en producción se
maneja con reintento, no se asume que no va a ocurrir.

### Configuración para LangChain
```python
# ChatGroq lee GROQ_API_KEY del entorno automáticamente
from langchain_groq import ChatGroq
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
```

### Configuración para CrewAI (CRÍTICA)
```python
# CrewAI enruta por LiteLLM: el prefijo "groq/" es obligatorio
import os
from crewai import LLM
llm = LLM(model=f"groq/{os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')}", temperature=0)
```

> **Instalación:** el extra es obligatorio → `pip install "crewai[litellm]" crewai-tools`.
> Desde CrewAI 1.x LiteLLM ya no viene incluido y Groq no es un proveedor nativo, así que sin
> ese extra `LLM(model="groq/...")` falla con `ImportError`. En el repo ya está en `pyproject.toml`.

## ⚠️ Problemas Comunes y Soluciones

### 1. Error de Autenticación o de proveedor en CrewAI
**Síntoma**: `AuthenticationError: Incorrect API key provided` / `LLM Provider NOT provided`
**Causa**: Falta `GROQ_API_KEY` en el entorno, o el modelo no lleva el prefijo del proveedor
**Solución**: Definir `GROQ_API_KEY` en `.env` (o en los Secrets de Colab) y usar `model="groq/openai/gpt-oss-120b"`

### 2. Error de Herramientas en CrewAI
**Síntoma**: `'Tool' object is not callable`
**Causa**: Mezclar decorador `@tool` de LangChain con CrewAI
**Solución**: Usar `BaseTool` de `crewai_tools`

### 3. Error de Parámetro Verbose
**Síntoma**: `ValidationError: Input should be a valid boolean`
**Causa**: Usar `verbose=2` en lugar de boolean
**Solución**: Usar `verbose=True` en Crew

## 🏗️ Patrones Arquitectónicos Implementados

| **Patrón** | **Notebook** | **Características** |
|------------|--------------|-------------------|
| **Monolítico** | 1-agent-fundamentals | Toda la lógica en una función, parsing manual |
| **Estructurado** | 2-agent-function-calling | JSON Schema, llamadas nativas |
| **Modular** | 3-langchain-agent | Separación de componentes, abstracciones |
| **Colaborativo** | 4-crewai-agent | Múltiples agentes especializados |

## 🔄 Comparación de Frameworks

| **Criterio** | **LangChain** | **CrewAI** |
|-------------|--------------|------------|
| **Especialización** | Agentes individuales complejos | Equipos colaborativos |
| **Complejidad** | Simple a moderada | Compleja, multi-paso |
| **Flexibilidad** | Muy alta, experimental | Estructurada, workflow-oriented |
| **Configuración** | Directa con `GROQ_API_KEY` | Requiere el prefijo `groq/` en el modelo |
| **Curva de aprendizaje** | Moderada | Baja para equipos |
| **Casos de uso** | Experimentación, prototipado | Workflows de producción |

## 📝 Actividades Prácticas

### Ejercicios Implementados
1. **Agente Básico**: Implementación desde cero con ReAct manual
2. **Function Calling**: Agente con Wikipedia usando JSON Schema
3. **LangChain Individual**: Agente con herramientas integradas
4. **Equipo CrewAI**: Investigador + Escritor colaborativo

### Casos de Uso Desarrollados
- **Investigación Automatizada**: Búsqueda y síntesis de información
- **Generación de Contenido**: Biografías basadas en investigación
- **Workflows Multi-agente**: Coordinación secuencial especializada

## 🎓 Preparación para IL2.2

### Conceptos Avanzados Siguientes
- **Memory Systems**: Sistemas de memoria persistente y contextual
- **Model Context Protocol (MCP)**: Estándar para integración de herramientas
- **Advanced Planning**: Algoritmos de planificación y re-planificación
- **Tool Integration**: APIs complejas y bases de datos

### Base Establecida
- ✅ Fundamentos sólidos de agentes inteligentes
- ✅ Experiencia con frameworks principales
- ✅ Configuraciones de producción para la API de Groq
- ✅ Patrones de colaboración entre agentes
- ✅ Debugging y troubleshooting de sistemas complejos

## 🔗 Recursos Adicionales

### Documentación Oficial
- [LangChain Agents Documentation](https://docs.langchain.com/oss/python/langchain/agents)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Groq Tool Use (Function Calling)](https://console.groq.com/docs/tool-use)

### Herramientas de Desarrollo
- [LangSmith](https://smith.langchain.com/) - Observabilidad para agentes LangChain
- [Groq Console](https://console.groq.com/) - API keys, modelos disponibles y límites de uso

### Troubleshooting y Soporte
- [GitHub Issues - CrewAI](https://github.com/crewAIInc/crewAI/issues)
- [LangChain Community](https://github.com/langchain-ai/langchain/discussions)

## 💡 Mejores Prácticas Identificadas

1. **Configuración de Entorno**: Verificar variables antes de ejecutar agentes
2. **Manejo de Errores**: Implementar validación robusta en herramientas
3. **Documentación de Herramientas**: Descripciones claras para mejor selección
4. **Debugging**: Usar modo verbose para observar flujo de decisiones
5. **Versionado**: Mantener compatibilidad entre versiones de frameworks
6. **Testing**: Probar configuraciones en entornos similares a producción