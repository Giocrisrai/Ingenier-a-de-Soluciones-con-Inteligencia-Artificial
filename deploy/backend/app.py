"""API FastAPI del agente del curso.

Endpoints:
  GET  /health   — liveness
  POST /chat     — valida (guardrails) → agente → sanitiza salida
  GET  /metrics  — contadores básicos para observabilidad (RA3.1)

Seguridad: rate limiting por IP (slowapi), validación de entrada con Pydantic,
guardrails de prompt injection / PII / filtro ético, y nunca expone trazas
internas al cliente.
"""
import logging

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

_METRICAS = {"total_requests": 0, "bloqueados": 0, "errores": 0}
_agente = AgentClient()


class ChatRequest(BaseModel):
    mensaje: str = Field(..., min_length=1, max_length=2000)
    historial: list[dict] = Field(default_factory=list)


class ChatResponse(BaseModel):
    respuesta: str
    bloqueado: bool = False
    motivo: str | None = None


@app.exception_handler(RateLimitExceeded)
def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Demasiadas solicitudes. Intenta más tarde."})


@app.get("/health")
def health():
    return {"status": "ok", "modo_demo": _agente.modo_demo}


@app.get("/metrics")
def metrics():
    return _METRICAS


@app.post("/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
def chat(request: Request, body: ChatRequest):
    _METRICAS["total_requests"] += 1
    validacion = guardrails.validar_entrada(body.mensaje)
    if not validacion.es_valida:
        _METRICAS["bloqueados"] += 1
        logger.info("entrada bloqueada: %s", validacion.motivo)
        return ChatResponse(respuesta="No puedo procesar esa solicitud.", bloqueado=True, motivo=validacion.motivo)
    try:
        salida = _agente.responder(validacion.texto_sanitizado, body.historial)
        salida = guardrails.sanitizar_pii(salida)
        return ChatResponse(respuesta=salida, bloqueado=False)
    except Exception:
        _METRICAS["errores"] += 1
        logger.exception("error al generar respuesta")  # detalle solo en logs
        return ChatResponse(respuesta="Ocurrió un error procesando tu solicitud.", bloqueado=False)
