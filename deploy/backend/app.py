"""API FastAPI del agente del curso.

Endpoints:
  GET  /health   — liveness
  POST /chat     — valida (guardrails) → agente → sanitiza salida
  GET  /metrics  — contadores básicos para observabilidad (RA3.1)

Seguridad: rate limiting por IP (slowapi + cabeceras del proxy, ver más abajo),
validación de entrada con Pydantic, guardrails de prompt injection / PII /
filtro ético sobre el mensaje, sobre cada turno del historial Y sobre la
conversación concatenada (validar turno a turno solo se evade troceando el
payload), presupuesto acumulado de caracteres (anti DoS / amplificación de
costo), y nunca se exponen trazas internas al cliente.

Lo que estos guardrails NO cubren está escrito sin adornos en el docstring de
`guardrails.py`. Léelo antes de usar esto como plantilla.
"""
import logging
import os
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

import guardrails
from agent import SYSTEM_PROMPT, AgentClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")


def _flag(nombre: str, por_defecto: str = "false") -> bool:
    return os.getenv(nombre, por_defecto).strip().lower() in {"1", "true", "yes", "si", "sí"}


# `get_remote_address` lee `request.client.host`. Detrás de un reverse proxy eso
# es la IP DEL PROXY, no la del usuario: todo el mundo compartiría el mismo
# cubo de 20/minuto y un solo atacante dejaría sin servicio a la clase entera.
# Para que devuelva la IP real, uvicorn arranca con `--proxy-headers` y
# `--forwarded-allow-ips` apuntando a la IP de Caddy (ver Dockerfile y
# docker-compose.prod.yml).
#
# ADVERTENCIA: confiar en X-Forwarded-For solo es seguro si delante hay un proxy
# de confianza que REESCRIBE la cabecera. Aquí lo hay (Caddy). Si este backend
# quedara expuesto directamente a Internet, cualquiera se saltaría el límite
# mandando `X-Forwarded-For: <ip inventada>` en cada petición. Por eso la lista
# de IPs de confianza nunca debe ser `*` en un servicio expuesto.
limiter = Limiter(key_func=get_remote_address)

# /docs, /redoc y /openapi.json: DESACTIVADOS por defecto.
# Caddy publica el backend en `/api/*` quitando el prefijo, así que dejarlos
# activos significa servir la consola interactiva de FastAPI en Internet:
# el catálogo completo de endpoints y un formulario para dispararlos. No aporta
# nada al usuario final y sí regala reconocimiento a quien busque qué atacar.
# Para desarrollo se encienden con ENABLE_DOCS=true en el .env.
_DOCS_ACTIVAS = _flag("ENABLE_DOCS")

app = FastAPI(
    title="Agente IA — Curso ISIA",
    version="1.0.0",
    docs_url="/docs" if _DOCS_ACTIVAS else None,
    redoc_url="/redoc" if _DOCS_ACTIVAS else None,
    openapi_url="/openapi.json" if _DOCS_ACTIVAS else None,
)
app.state.limiter = limiter

MAX_MENSAJE = 2000
MAX_HISTORIAL_ITEMS = 20
MAX_PRESUPUESTO_CHARS = 8000  # límite acumulado mensaje + historial (anti DoS / costo)

_METRICAS = {"total_requests": 0, "bloqueados": 0, "errores": 0}
_agente = AgentClient()


class HistorialItem(BaseModel):
    # Solo turnos de usuario/asistente: el cliente no puede inyectar un turno
    # 'system' ni 'tool', que es la forma más directa de sobrescribir el rol.
    #
    # OJO, esto NO es "protección contra prompt injection": el cliente sigue
    # pudiendo mandar un turno 'assistant' inventado con el contenido que
    # quiera ("claro, aquí van mis instrucciones internas: …") y el modelo lo
    # leerá como si lo hubiera dicho él. Es el self-priming jailbreak. Contra
    # eso, lo único que hay aquí es que el contenido de cada turno pasa por los
    # guardrails y que la conversación se revalida concatenada. Un backend que
    # de verdad quiera cerrarlo no debe aceptar el historial del cliente:
    # guarda la conversación en el servidor y el cliente solo manda un id.
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=MAX_MENSAJE)


class ChatRequest(BaseModel):
    mensaje: str = Field(..., min_length=1, max_length=MAX_MENSAJE)
    historial: list[HistorialItem] = Field(default_factory=list, max_length=MAX_HISTORIAL_ITEMS)


class ChatResponse(BaseModel):
    respuesta: str
    bloqueado: bool = False
    motivo: str | None = None


def _bloquear(motivo: str) -> ChatResponse:
    _METRICAS["bloqueados"] += 1
    logger.info("entrada bloqueada: %s", motivo)
    return ChatResponse(respuesta="No puedo procesar esa solicitud.", bloqueado=True, motivo=motivo)


@app.exception_handler(RateLimitExceeded)
def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Demasiadas solicitudes. Intenta más tarde."})


@app.get("/health")
def health():
    return {"status": "ok", "modo_demo": _agente.modo_demo}


@app.get("/metrics")
def metrics():
    # NOTA didáctica (IL3.5): endpoint abierto a propósito para la demo de
    # observabilidad (RA3.1). En producción protégelo (token/API key o IP interna).
    return _METRICAS


@app.post("/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
def chat(request: Request, body: ChatRequest):
    _METRICAS["total_requests"] += 1

    # 1) Validar el mensaje del usuario
    validacion = guardrails.validar_entrada(body.mensaje)
    if not validacion.es_valida:
        return _bloquear(validacion.motivo)

    # 2) Validar y sanear cada turno del historial (no confiar en el cliente)
    presupuesto = len(body.mensaje)
    historial_saneado: list[dict] = []
    for item in body.historial:
        v = guardrails.validar_entrada(item.content)
        if not v.es_valida:
            return _bloquear(f"Historial inválido: {v.motivo}")
        presupuesto += len(item.content)
        historial_saneado.append(
            {"role": item.role, "content": guardrails.sanitizar_pii(item.content)}
        )

    # 3) Presupuesto acumulado (anti amplificación de costo / DoS)
    if presupuesto > MAX_PRESUPUESTO_CHARS:
        return _bloquear(f"La conversación supera el límite de {MAX_PRESUPUESTO_CHARS} caracteres.")

    # 4) Revalidar la conversación CONCATENADA.
    #    Los pasos 1 y 2 miran cada turno por separado, y eso se evade
    #    troceando la frase: historial ["ignora las", "instrucciones"] +
    #    mensaje "anteriores" pasa turno a turno, pero el modelo recibe la
    #    frase completa. Se valida lo que va a leer el modelo, no las piezas.
    turnos = [i.content for i in body.historial] + [body.mensaje]
    completa = guardrails.validar_conversacion(turnos)
    if not completa.es_valida:
        return _bloquear(f"Conversación completa: {completa.motivo}")

    # 5) Ejecutar el agente y revisar la salida
    try:
        salida = _agente.responder(validacion.texto_sanitizado, historial_saneado)
        salida = guardrails.sanitizar_pii(salida)

        # Guardrail de SALIDA. Solo dos cosas, a propósito:
        #   a) sanitizar PII (arriba), y
        #   b) detectar que la respuesta repita literalmente el system prompt.
        # Lo que NO hacemos es pasar el filtro ético (`es_no_etico`) por la
        # respuesta: un asistente educativo tiene motivos legítimos para
        # escribir "no puedo explicarte cómo fabricar una bomba" o para hablar
        # de desinformación, y bloquearlo rompería respuestas correctas. Un
        # filtro léxico de salida da además una falsa sensación de seguridad:
        # el modelo puede decir lo mismo con otras palabras. Si esto se
        # llevara a producción, la capa de salida debe ser un clasificador,
        # no una lista de palabras.
        if guardrails.hay_fuga_de_instrucciones(salida, SYSTEM_PROMPT):
            return _bloquear("La respuesta filtraba las instrucciones del sistema.")

        return ChatResponse(respuesta=salida, bloqueado=False)
    except Exception:
        _METRICAS["errores"] += 1
        logger.exception("error al generar respuesta")  # detalle solo en logs
        return ChatResponse(respuesta="Ocurrió un error procesando tu solicitud.", bloqueado=False)
