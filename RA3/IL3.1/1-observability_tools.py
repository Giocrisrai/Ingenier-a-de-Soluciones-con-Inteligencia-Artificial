"""
IL3.1: Herramientas de Observabilidad y Metricas
=================================================
Demuestra logging estructurado con timestamps, recoleccion de metricas
(tiempos de respuesta, uso de tokens, tasa de errores) y un wrapper
de agente que registra todas las interacciones.

Ejecutar: python 1-observability_tools.py
"""

import logging
import time
import random
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import List

# --- Configuracion de logging estructurado con timestamps ---

formato_log = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

manejador_consola = logging.StreamHandler()
manejador_consola.setFormatter(formato_log)

logger = logging.getLogger("observabilidad")
logger.setLevel(logging.DEBUG)
logger.addHandler(manejador_consola)


# --- Recolector de metricas ---

@dataclass
class RegistroMetrica:
    """Registro individual de una interaccion."""
    timestamp: str
    tiempo_respuesta_ms: float
    tokens_entrada: int
    tokens_salida: int
    exitoso: bool
    modelo: str


class RecolectorMetricas:
    """Recolecta y resume metricas de rendimiento de un agente."""

    def __init__(self):
        self.registros: List[RegistroMetrica] = []

    def registrar(self, tiempo_ms: float, tokens_in: int, tokens_out: int,
                  exitoso: bool, modelo: str = "gpt-4o-mini"):
        registro = RegistroMetrica(
            timestamp=datetime.now().isoformat(),
            tiempo_respuesta_ms=round(tiempo_ms, 2),
            tokens_entrada=tokens_in,
            tokens_salida=tokens_out,
            exitoso=exitoso,
            modelo=modelo,
        )
        self.registros.append(registro)

    def resumen(self) -> dict:
        """Devuelve un resumen con estadisticas agregadas."""
        if not self.registros:
            return {"total_peticiones": 0}

        tiempos = [r.tiempo_respuesta_ms for r in self.registros]
        total_tokens = sum(r.tokens_entrada + r.tokens_salida for r in self.registros)
        errores = sum(1 for r in self.registros if not r.exitoso)

        return {
            "total_peticiones": len(self.registros),
            "tiempo_promedio_ms": round(sum(tiempos) / len(tiempos), 2),
            "tiempo_maximo_ms": round(max(tiempos), 2),
            "tiempo_minimo_ms": round(min(tiempos), 2),
            "total_tokens": total_tokens,
            "tasa_errores_pct": round((errores / len(self.registros)) * 100, 2),
        }


# --- Wrapper de agente con observabilidad ---

class AgenteObservable:
    """Agente simulado que registra cada interaccion con metricas."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.metricas = RecolectorMetricas()
        self.logger = logging.getLogger(f"agente.{nombre}")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            self.logger.addHandler(manejador_consola)

    def procesar(self, mensaje: str) -> str:
        """Simula el procesamiento de un mensaje con metricas."""
        self.logger.info(f"Entrada: {mensaje!r}")
        inicio = time.perf_counter()

        # Simulacion: tiempo de respuesta y posible error aleatorio
        tiempo_simulado = random.uniform(50, 500)  # milisegundos
        time.sleep(tiempo_simulado / 1000)
        es_error = random.random() < 0.15  # 15% de probabilidad de error

        duracion_ms = (time.perf_counter() - inicio) * 1000
        tokens_in = len(mensaje.split()) * 2  # estimacion simple
        tokens_out = random.randint(20, 150)

        if es_error:
            self.logger.warning(f"Error simulado al procesar: {mensaje!r}")
            self.metricas.registrar(duracion_ms, tokens_in, 0, exitoso=False)
            return "[ERROR] No se pudo generar respuesta"

        respuesta = f"Respuesta generada para: {mensaje}"
        self.metricas.registrar(duracion_ms, tokens_in, tokens_out, exitoso=True)
        self.logger.info(f"Salida ({duracion_ms:.1f}ms, {tokens_in}+{tokens_out} tokens)")
        return respuesta

    def reporte(self):
        """Imprime un reporte estructurado de metricas."""
        resumen = self.metricas.resumen()
        self.logger.info("=== Reporte de Metricas ===")
        print(json.dumps(resumen, indent=2, ensure_ascii=False))


# --- Ejecucion de demostracion ---

if __name__ == "__main__":
    agente = AgenteObservable("demo-v1")

    mensajes = [
        "Explica que es machine learning",
        "Resume este articulo sobre IA",
        "Traduce esta oracion al ingles",
        "Genera un plan de estudio semanal",
        "Que es la observabilidad en sistemas de IA",
    ]

    print("=" * 60)
    print("DEMOSTRACION: Observabilidad en Agentes de IA")
    print("=" * 60)

    for msg in mensajes:
        resultado = agente.procesar(msg)
        print(f"  -> {resultado}\n")

    print("=" * 60)
    agente.reporte()
