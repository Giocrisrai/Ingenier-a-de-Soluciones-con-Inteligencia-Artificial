# Antes de la clase — checklist del docente

Documento interno. Reúne lo que conviene comprobar y anticipar antes de cada sesión, con los
riesgos reales detectados al probar el material. Los alumnos tienen su propia
[Guía del Estudiante](GUIA_DEL_ESTUDIANTE.md).

---

## 1. El día antes

```bash
git pull
uv sync
uv run python scripts/verify_groq.py
```

Si eso termina en verde, el entorno está listo. `verify_groq.py` comprueba la API key, el SDK
de Groq, `ChatGroq` y los embeddings locales.

**Revisa tu cuota antes de empezar.** El modelo grande tiene solo **100.000 tokens al día** y
es el límite que se agota primero. Si estuviste preparando la clase ejecutando notebooks, es
muy posible que ya la hayas consumido. Compruébalo en
[console.groq.com](https://console.groq.com/) → Usage.

---

## 2. Lo que hay que pedir a los alumnos con antelación

| Qué | Por qué |
|---|---|
| Crear su **propia** API key en console.groq.com | Los límites son por cuenta. Si comparten, se quedan todos sin cuota. |
| Ejecutar `verify_groq.py` **en casa** | Descarga ~470 MB del modelo de embeddings. Con 30 personas a la vez sobre el wifi de la sala, es el cuello de botella más probable de todo el curso. |
| Tener el `.env` creado y funcionando | Es el fallo nº 1 en la primera sesión. |

Esto aplica sobre todo antes de **RA1/IL1.3** (RAG), que es donde entran los embeddings.

---

## 3. Riesgos por módulo

### RA1/IL1.3 e IL1.4 — RAG
- La **descarga de 470 MB** ocurre aquí si no la hicieron antes.
- La app Streamlit de IL1.4 (`1-evaluation-rag.py`) gasta bastante cuota en la pestaña de
  evaluación completa (≈5 llamadas por caso × 3 casos). Si la vas a demostrar, ponte antes
  `GROQ_MODEL=llama-3.1-8b-instant`.

### RA1/IL1.2 — Prompt engineering
- `4-advanced-techniques.ipynb` es de los que más queman cuota (self-consistency y
  árbol de pensamientos hacen muchas llamadas).

### RA2/IL2.1 e IL2.2 — Agentes
- Los notebooks con herramientas usan **modelos distintos a propósito**, y está medido:
  por SDK crudo el 8B es más fiable que el 70B, por LangChain es al revés, y en cadenas
  multi-paso ninguno de los dos, por eso se usa `openai/gpt-oss-20b`. Si un alumno pregunta
  por qué no es todo el mismo modelo, la respuesta está en el README de IL2.1.
- El error `400 tool_use_failed` puede salir en vivo. **No es un fallo del código**: es el
  modelo generando mal la llamada. Los agentes del curso lo reintentan.
- En Colab, instalar CrewAI tarda varios minutos. No lo dejes para el momento.

### RA2/IL2.3 — Planificación
- ⚠️ **`Swarm_101.ipynb` no está validado de punta a punta.** Es el único del curso.
  Depende de una librería archivada por OpenAI. **No lo pongas como demo en vivo.**
  Sirve como lectura y, sobre todo, como ejemplo de lo que cuesta integrar una librería
  con un proveedor para el que no fue escrita (los tres parches están explicados dentro).
- De los 19 archivos del módulo, **11 no necesitan API key**: son simulaciones puras.
  La tabla está en el README del módulo.

### RA3/IL3.3 — Seguridad y ética
- Es el notebook que **más cuota consume** de todo RA3 (más de 30 llamadas al modelo grande).
  Si ya usaste la key ese día, hay riesgo real de `429` en clase. Ten preparado
  `GROQ_MODEL=llama-3.1-8b-instant`.

### RA3/IL3.5 — Despliegue en AWS
- El paso a paso está revisado comando a comando, pero **no se ha probado en una EC2 real**.
- El navegador **siempre** mostrará aviso de certificado no confiable al abrir `https://<IP>`:
  Caddy emite uno self-signed. Anticípalo antes de proyectar.
- Si el chat responde `[modo demo]`, es que el backend arrancó sin `GROQ_API_KEY`.

---

## 4. Errores que van a aparecer en vivo

Todos están explicados con su solución en la
[Guía del Estudiante](GUIA_DEL_ESTUDIANTE.md#6-errores-frecuentes). Los tres más probables:

| Error | Qué decir |
|---|---|
| `429 tokens per day` | Se acabó la cuota diaria de ese modelo. Cambiar a `llama-3.1-8b-instant`, que tiene 5× más. |
| `400 tool_use_failed` | El modelo generó mal la llamada a la herramienta. No es su código. Reintentar. |
| `401` de LangSmith | LangSmith es opcional. Dejar `LANGSMITH_TRACING="false"`. |

---

## 5. Estado de verificación del material

Última verificación completa: **agosto 2026**, tras la migración a Groq.

| Qué | Estado |
|---|---|
| Instalación desde cero (`git clone` + `uv sync` + verificación) | ✅ Probado, ~3 min |
| Tests del artefacto desplegable | ✅ 17/17 |
| Scripts `.py` | ✅ Todos compilan; los de simulación, ejecutados |
| Notebooks | ✅ Ejecutados contra Groq, **excepto `Swarm_101`** |
| CI (GitHub Actions) | ✅ Verde: tests, Docker e2e, Trivy |
| Despliegue en EC2 real | ❌ No probado |
| Windows y Linux | ❌ No probado (todo verificado en macOS) |

---

## 6. Si algo se rompe en clase

1. `uv run python scripts/verify_groq.py` te dice en 10 segundos si el problema es la key,
   la red o el entorno.
2. Si es cuota, cambia `GROQ_MODEL` a `llama-3.1-8b-instant` en tu `.env` y reinicia el kernel.
3. Los módulos de RA2/IL2.3 y RA3 tienen scripts `.py` que **no necesitan API key**: son un
   buen plan B para seguir la clase sin conexión al modelo.
