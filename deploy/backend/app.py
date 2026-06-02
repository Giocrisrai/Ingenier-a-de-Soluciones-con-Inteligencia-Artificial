"""API FastAPI del agente del curso.

Endpoints:
  GET  /health   — liveness
  POST /chat     — valida (guardrails) → agente → sanitiza salida
  GET  /metrics  — contadores básicos para observabilidad (RA3.1)

Seguridad: rate limiting por IP (slowapi), validación de entrada con Pydantic,
guardrails de prompt injection / PII / filtro ético sobre el mensaje Y cada turno
del historial (el cliente nunca puede inyectar un turno 'system'), presupuesto
acumulado de caracteres (anti DoS / amplificación de costo), y nunca se exponen
trazas internas al cliente.
"""
import logging
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

import guardrails
from agent import AgentClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Agente IA — Curso ISIA", version="1.0.0")
app.state.limiter = limiter

MAX_MENSAJE = 2000
MAX_HISTORIAL_ITEMS = 20
MAX_PRESUPUESTO_CHARS = 8000  # límite acumulado mensaje + historial (anti DoS / costo)

_METRICAS = {"total_requests": 0, "bloqueados": 0, "errores": 0}
_agente = AgentClient()


class HistorialItem(BaseModel):
    # Solo turnos de usuario/asistente: el cliente nunca puede inyectar un turno
    # 'system' o 'tool' (evita override del rol / prompt injection).
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

    # 4) Ejecutar el agente y sanitizar la salida
    try:
        salida = _agente.responder(validacion.texto_sanitizado, historial_saneado)
        salida = guardrails.sanitizar_pii(salida)
        return ChatResponse(respuesta=salida, bloqueado=False)
    except Exception:
        _METRICAS["errores"] += 1
        logger.exception("error al generar respuesta")  # detalle solo en logs
        return ChatResponse(respuesta="Ocurrió un error procesando tu solicitud.", bloqueado=False)
