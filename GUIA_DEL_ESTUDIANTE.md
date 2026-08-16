# Guía del Estudiante

Todo lo que necesitas saber para que el curso te funcione sin sustos.
Si algo te falla, **busca el error en la sección [Errores frecuentes](#6-errores-frecuentes)**:
están todos los que aparecen de verdad, con su causa y su solución.

Para instalar el entorno paso a paso, ve al [README](README.md). Esta guía es lo que
viene después: cómo funciona el curso por dentro y qué hacer cuando algo no sale.

---

## 1. En 3 pasos

```bash
uv sync                                  # 1. instalar (tarda ~3 min la primera vez)
cp .env.example .env                     # 2. crear tu archivo de credenciales
                                         #    y pegar tu GROQ_API_KEY dentro
uv run python scripts/verify_groq.py     # 3. comprobar que todo responde
```

Si el paso 3 termina con **"Listo: Groq y los embeddings locales funcionan correctamente"**,
ya puedes abrir cualquier notebook del curso.

Tu API key se saca gratis en [console.groq.com](https://console.groq.com/) →
**API Keys** → **Create API Key**. Empieza por `gsk_`. **No hace falta tarjeta de crédito.**
Cópiala en ese momento: no se vuelve a mostrar.

---

## 2. ¿Trabajas en Colab o en tu computador?

Los notebooks funcionan **igual en los dos sitios**. Lo único que cambia es dónde guardas la key.

| | Colab | En tu computador |
|---|---|---|
| Dónde va la key | Menú 🔑 **Secrets** → nombre `GROQ_API_KEY` | Archivo `.env` en la raíz del repo |
| Dependencias | Las instala la primera celda del notebook | Ya las instaló `uv sync` |
| Qué más hacer | Activar el acceso del notebook al Secret | Nada |

Los notebooks detectan solos dónde están. No tienes que cambiar ni una línea de código.

---

## 3. Los modelos del curso

El curso usa **Groq** como proveedor. No usamos un solo modelo: cada uno sirve para algo distinto.

| Variable | Modelo | Para qué se usa |
|---|---|---|
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Por defecto. Razonamiento, agentes de LangChain. |
| `GROQ_MODEL_FAST` | `llama-3.1-8b-instant` | Tareas simples y todo lo que haga muchas llamadas. |
| `GROQ_MODEL_TOOLS` | `openai/gpt-oss-20b` | Agentes que encadenan varias herramientas seguidas. |
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | Embeddings, **en tu propio computador**. |

Ya vienen configurados en `.env.example`: no tienes que tocarlos.

> **¿Por qué tres modelos y no uno?** Porque lo medimos. El modelo más grande no siempre es
> el mejor: en las llamadas a herramientas, el pequeño acierta el formato más veces que el
> grande, y en cadenas de varios pasos ninguno de los dos es fiable. Cada notebook lleva un
> comentario explicando por qué usa el que usa. Lo verás en detalle en **RA2/IL2.1**.

### Los embeddings no salen de tu computador

Groq **no ofrece** un servicio de embeddings, así que el curso usa un modelo que se ejecuta
localmente. Esto tiene tres consecuencias prácticas:

- Es **gratis** y no consume tu cuota de Groq.
- Funciona **sin conexión** una vez descargado.
- La **primera vez descarga unos 470 MB**. Solo la primera vez, luego queda en caché.

⚠️ **Haz esa primera descarga en casa, no en clase.** Si 30 personas la lanzan a la vez sobre
el wifi de la sala, va a ir muy lento. Basta con que ejecutes una vez
`uv run python scripts/verify_groq.py`.

---

## 4. La cuota gratuita (esto es lo que más confunde)

La capa gratuita de Groq tiene límites. El que se agota primero **no** es el de peticiones,
sino el de **tokens al día**:

| Modelo | Peticiones/min | Peticiones/día | Tokens/min | **Tokens/día** |
|---|---|---|---|---|
| `llama-3.3-70b-versatile` | 30 | 1.000 | 12.000 | **100.000** |
| `llama-3.1-8b-instant` | 30 | 14.400 | 6.000 | **500.000** |

*Valores de agosto 2026. Los vigentes están siempre en
[la documentación de Groq](https://console.groq.com/docs/rate-limits) y en tu consola.*

**Consejo que te va a ahorrar tiempo:** mientras pruebas y te equivocas, usa el modelo rápido.
Deja el grande para la ejecución final.

```bash
# en tu .env, mientras experimentas
GROQ_MODEL="llama-3.1-8b-instant"
```

Los límites son **por cuenta**, así que cada uno debe usar su propia API key. No compartas
la tuya con un compañero: os quedaréis los dos sin cuota.

---

## 4.b Si te quedas sin cuota: el plan B (Mistral)

Groq es el proveedor del curso, pero **no estás atado a él**. Si agotas la cuota diaria y
necesitas seguir trabajando hoy, puedes cambiar a [Mistral](https://console.mistral.ai/),
que también es gratis y tampoco pide tarjeta.

Estos números **los medimos nosotros** contra la API real (agosto 2026), no son de folleto:

| | Groq `llama-3.3-70b` | Groq `llama-3.1-8b` | Mistral `mistral-small-latest` |
|---|---|---|---|
| Peticiones/min | 30 | 30 | **50** |
| Tokens/min | 12.000 | 6.000 | **50.000** |
| Tokens/día | 100.000 | 500.000 | **sin tope diario declarado** |
| Embeddings | no ofrece | no ofrece | **sí** (`mistral-embed`) |

### Cómo cambiar

1. Saca tu key en [console.mistral.ai](https://console.mistral.ai/api-keys) y añádela al `.env`:

   ```env
   MISTRAL_API_KEY="tu_key_aqui"
   ```

2. En el notebook donde estés, sustituye la línea que crea el modelo:

   ```python
   # En vez de esto:
   llm = ChatGroq(model=MODELO, temperature=0)

   # Usa esto:
   from langchain_openai import ChatOpenAI
   llm = ChatOpenAI(
       model="mistral-small-latest",
       base_url="https://api.mistral.ai/v1",
       api_key=os.environ["MISTRAL_API_KEY"],
       temperature=0,
   )
   ```

   El resto del notebook **no cambia**: es el mismo protocolo, como viste en IL1.1.
   Necesitarás `uv add langchain-openai` si no lo tienes.

> **Ojo:** cambiar de proveedor cambia el modelo, y **cada modelo se comporta distinto**.
> En nuestras pruebas Mistral acertó 10/10 las llamadas a herramientas, mejor que los Llama
> de Groq. Pero las respuestas no serán idénticas: si estás comparando resultados con un
> compañero, aseguraos de usar el mismo proveedor.

---

## 5. Qué necesita cada módulo

Antes de empezar un módulo, mira aquí qué te hace falta.

| Módulo | Archivos que piden API key | Archivos sin API key | ¿Descarga embeddings? |
|---|---|---|---|
| **RA1/IL1.1** Primeros pasos | 5 | 0 | No |
| **RA1/IL1.2** Prompt engineering | 5 | 0 | No |
| **RA1/IL1.3** RAG | 3 | 1 | **Sí (470 MB)** |
| **RA1/IL1.4** Evaluación | 3 | 0 | **Sí (470 MB)** |
| **RA2/IL2.1** Agentes | 4 | 0 | No |
| **RA2/IL2.2** Memoria y herramientas | 3 | 0 | No |
| **RA2/IL2.3** Planificación | 8 | **11** | No |
| **RA2/IL2.4** Documentación | 1 | 1 | No |
| **RA3/IL3.1** Observabilidad | 1 | 1 | No |
| **RA3/IL3.2** Trazabilidad | 1 | 1 | No |
| **RA3/IL3.3** Seguridad y ética | 1 | 1 | No |
| **RA3/IL3.4** Escalabilidad | 1 | 1 | No |
| **RA3/IL3.5** Despliegue en AWS | 0 | 1 | No |

En **RA2/IL2.3** y en todo **RA3**, los archivos `.py` numerados son en su mayoría
**simulaciones que no llaman al modelo**: puedes ejecutarlos sin gastar nada de cuota.
Los `.ipynb` sí llaman al modelo. Cada README de módulo lo detalla archivo por archivo.

---

## 6. Errores frecuentes

### `AssertionError: Falta GROQ_API_KEY`

No encuentra tu credencial. Por orden de probabilidad:

1. No creaste el `.env` (solo existe `.env.example`). → `cp .env.example .env`
2. Lo creaste **dentro de una carpeta** `RA1/…` en vez de en la raíz del repo.
3. Escribiste espacios alrededor del `=`. Debe ser `GROQ_API_KEY="gsk_..."`, sin espacios.
4. En Colab: guardaste el Secret pero no activaste su acceso para ese notebook.

Comprueba con: `uv run python scripts/verify_groq.py`

---

### `429 - rate_limit_exceeded`

Agotaste un límite. **Lee el mensaje del error**, porque te dice cuál y cuánto esperar:

- Si dice **`tokens per minute (TPM)`** → espera un minuto y vuelve a ejecutar. No es grave.
- Si dice **`tokens per day (TPD)`** → agotaste la cuota diaria de ese modelo. Cambia a
  `GROQ_MODEL="llama-3.1-8b-instant"` en tu `.env` (tiene 5 veces más) o continúa mañana.

No es un fallo de tu código.

---

### `400 - tool_use_failed`

El modelo intentó llamar a una herramienta pero generó el formato mal. **Es un fallo del
modelo, no tuyo.** Ocurre de forma intermitente y es normal: por eso los agentes del curso
lo manejan reintentando (lo verás en `RA2/IL2.2/3-herramientas-externas.ipynb`).

Si te pasa: vuelve a ejecutar la celda. Si te pasa siempre en el mismo sitio, revisa que el
notebook esté usando el modelo que le corresponde (mira el comentario junto a `MODELO = ...`).

---

### `LangSmithAuthError: 401 Unauthorized` o `LangSmithMissingAPIKeyWarning`

LangSmith es **opcional** y solo se usa en un notebook de RA1/IL1.4 y en RA3. Si no tienes
cuenta, no pasa nada: el material funciona igual.

Por eso `.env.example` trae `LANGSMITH_TRACING="false"`. Si ves estos errores es que lo
pusiste en `"true"` sin rellenar `LANGSMITH_API_KEY`. Déjalo en `"false"` hasta que tengas
una cuenta en [smith.langchain.com](https://smith.langchain.com/).

---

### `Failed to build tiktoken` / `error: failed to run custom build command for pyo3-ffi`

Le pasa sobre todo en **Windows**. El mensaje clave está al final del error:

```
error: the configured Python interpreter version (3.14) is newer than
       PyO3's maximum supported version (3.13)
```

**Qué ocurre:** tu Python es más nuevo que las versiones para las que existe una
versión precompilada de esa librería, así que `uv` intenta compilarla desde código
Rust y falla.

**Solución:** actualiza el repo. El proyecto fija la versión de Python en el archivo
`.python-version`, y `uv` la descarga sola si no la tienes:

```bash
git pull
uv sync
```

No necesitas desinstalar tu Python ni instalar Rust. `uv` usa la versión del
proyecto sin tocar la del sistema.

---

### `%pip install` no instala nada en local

El entorno que crea `uv sync` **no incluye `pip`**, así que una celda con `%pip install`
falla en tu computador (en Colab sí funciona). Si necesitas instalar algo puntual, usa uv:

```python
import sys
!uv pip install -q --python {sys.executable} nombre-del-paquete
```

Solo hay un notebook del curso que instala algo en local (`RA2/IL2.3/Swarm_101.ipynb`,
porque su librería no está en PyPI) y ya lo hace de la forma correcta.

---

### `ModuleNotFoundError: No module named 'groq'` (o `langchain_groq`, `crewai`…)

Estás usando un Python distinto al del proyecto.

- **En local:** ejecuta con `uv run python …` o activa el entorno (`source .venv/bin/activate`).
  En VS Code / Jupyter, elige el kernel que apunta a `.venv` del proyecto.
- **En Colab:** ejecuta la primera celda del notebook, que es la que instala las dependencias.

Comprueba el entorno con: `uv run python scripts/verify_env.py`

---

### La descarga de embeddings se queda parada

Son ~470 MB la primera vez. Si va muy lento, es la red. Déjalo terminar: solo ocurre una vez
y luego queda en caché en tu disco.

---

### Una celda se queda ejecutando para siempre

Comprueba si esa celda pide algo por teclado (`input(...)`). En `RA1/IL1.1/3-langchain_streaming.ipynb`
hay un chat interactivo que espera a que escribas. Escribe en el cuadro que aparece, o
interrumpe el kernel (⏹) y sáltate esa celda.

---

## 7. Seguridad: la regla que no se salta

**Nunca imprimas tu API key, ni siquiera unos pocos caracteres.**

Los notebooks guardan sus salidas **dentro del propio archivo `.ipynb`**. Si imprimes la key
y luego haces `git commit`, esa salida se sube a GitHub y queda en el historial para siempre.
Enseñar "solo el principio y el final" también publica parte de tu secreto.

```python
print("API Key:", api_key)                        # MAL
print("API Key:", api_key[:7] + "..." )           # TAMBIÉN MAL
print("API Key configurada:", api_key.startswith("gsk_"))   # BIEN
```

El archivo `.env` **nunca se sube**: ya está en `.gitignore`. Si alguna vez publicas una key
por accidente, no basta con borrarla del código: hay que **revocarla** en
[console.groq.com](https://console.groq.com/) y generar una nueva.

Este tema se trabaja a fondo en **RA3/IL3.3**.

---

## 8. Si nada de esto resuelve tu problema

1. Ejecuta `uv run python scripts/verify_env.py` y `uv run python scripts/verify_groq.py`,
   y guarda la salida.
2. Anota el **mensaje de error completo** y en qué notebook y celda ocurrió.
3. Consulta el README del módulo: cada uno tiene su sección de requisitos previos.

Con esos tres datos, el problema se resuelve en un minuto.
