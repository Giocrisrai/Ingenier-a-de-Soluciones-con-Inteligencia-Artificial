"""
IL3.2: Analisis de Trazabilidad y Logs
=======================================
Demuestra generacion de trace IDs unicos, logging estructurado en JSON,
seguimiento de linea temporal de ejecucion, y un analizador de trazas.

Ejecutar: python 1-traceability_analysis.py
"""

import uuid
import json
import time
import random
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional


# --- Modelo de una traza ---

@dataclass
class Evento:
    """Evento individual dentro de una traza."""
    etapa: str
    inicio_ms: float
    duracion_ms: float
    estado: str  # "ok" o "error"
    detalle: str = ""


@dataclass
class Traza:
    """Traza completa de una peticion al agente."""
    trace_id: str
    timestamp: str
    mensaje_entrada: str
    eventos: List[Evento] = field(default_factory=list)
    respuesta_final: Optional[str] = None

    def agregar_evento(self, etapa: str, inicio_ms: float,
                       duracion_ms: float, estado: str = "ok", detalle: str = ""):
        self.eventos.append(Evento(etapa, round(inicio_ms, 2),
                                   round(duracion_ms, 2), estado, detalle))

    def duracion_total_ms(self) -> float:
        return round(sum(e.duracion_ms for e in self.eventos), 2)

    def a_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)


# --- Agente trazable ---

class AgenteTrazable:
    """Agente que genera trazas estructuradas para cada peticion."""

    def __init__(self):
        self.historial_trazas: List[Traza] = []

    def procesar(self, mensaje: str) -> Traza:
        """Procesa un mensaje simulando multiples etapas con trazabilidad."""
        trace_id = str(uuid.uuid4())[:12]
        traza = Traza(
            trace_id=trace_id,
            timestamp=datetime.now().isoformat(),
            mensaje_entrada=mensaje,
        )

        tiempo_base = time.perf_counter()

        # Etapa 1: Validacion de entrada
        inicio = (time.perf_counter() - tiempo_base) * 1000
        time.sleep(random.uniform(0.01, 0.03))
        duracion = (time.perf_counter() - tiempo_base) * 1000 - inicio
        traza.agregar_evento("validacion_entrada", inicio, duracion, "ok",
                             f"Longitud: {len(mensaje)} caracteres")

        # Etapa 2: Clasificacion de intencion
        inicio = (time.perf_counter() - tiempo_base) * 1000
        time.sleep(random.uniform(0.05, 0.15))
        duracion = (time.perf_counter() - tiempo_base) * 1000 - inicio
        intencion = random.choice(["consulta", "calculo", "resumen", "traduccion"])
        traza.agregar_evento("clasificacion_intencion", inicio, duracion, "ok",
                             f"Intencion detectada: {intencion}")

        # Etapa 3: Generacion de respuesta (puede fallar)
        inicio = (time.perf_counter() - tiempo_base) * 1000
        time.sleep(random.uniform(0.1, 0.3))
        duracion = (time.perf_counter() - tiempo_base) * 1000 - inicio
        fallo = random.random() < 0.1
        if fallo:
            traza.agregar_evento("generacion_respuesta", inicio, duracion, "error",
                                 "Timeout simulado en modelo")
            traza.respuesta_final = "[ERROR] Fallo en generacion"
        else:
            traza.agregar_evento("generacion_respuesta", inicio, duracion, "ok",
                                 f"Modelo: gpt-4o-mini, tokens_salida: {random.randint(30, 200)}")
            traza.respuesta_final = f"Respuesta para '{mensaje}' (intencion: {intencion})"

        self.historial_trazas.append(traza)
        return traza


# --- Analizador de trazas ---

class AnalizadorTrazas:
    """Analiza un conjunto de trazas y genera un resumen."""

    @staticmethod
    def resumir(trazas: List[Traza]) -> dict:
        total = len(trazas)
        errores = sum(1 for t in trazas
                      if any(e.estado == "error" for e in t.eventos))
        duraciones = [t.duracion_total_ms() for t in trazas]

        # Etapas mas lentas en promedio
        tiempos_por_etapa: dict[str, list] = {}
        for t in trazas:
            for e in t.eventos:
                tiempos_por_etapa.setdefault(e.etapa, []).append(e.duracion_ms)

        promedio_por_etapa = {
            etapa: round(sum(vals) / len(vals), 2)
            for etapa, vals in tiempos_por_etapa.items()
        }

        return {
            "total_trazas": total,
            "trazas_con_error": errores,
            "tasa_exito_pct": round(((total - errores) / total) * 100, 1) if total else 0,
            "duracion_promedio_ms": round(sum(duraciones) / len(duraciones), 2) if duraciones else 0,
            "duracion_maxima_ms": round(max(duraciones), 2) if duraciones else 0,
            "promedio_por_etapa_ms": promedio_por_etapa,
        }


# --- Ejecucion de demostracion ---

if __name__ == "__main__":
    agente = AgenteTrazable()

    mensajes_prueba = [
        "Que es la trazabilidad en IA",
        "Calcula la raiz cuadrada de 144",
        "Resume el concepto de observabilidad",
        "Traduce 'hola mundo' al ingles",
        "Explica que es un trace ID",
        "Como funciona el logging estructurado",
    ]

    print("=" * 60)
    print("DEMOSTRACION: Trazabilidad en Agentes de IA")
    print("=" * 60)

    for msg in mensajes_prueba:
        traza = agente.procesar(msg)
        print(f"\n[Traza {traza.trace_id}] {msg}")
        print(f"  Duracion total: {traza.duracion_total_ms():.2f} ms")
        for evento in traza.eventos:
            indicador = "OK" if evento.estado == "ok" else "ERR"
            print(f"    [{indicador}] {evento.etapa}: {evento.duracion_ms:.2f} ms - {evento.detalle}")

    # Mostrar una traza completa en JSON
    print("\n" + "=" * 60)
    print("EJEMPLO DE TRAZA COMPLETA (JSON):")
    print(agente.historial_trazas[0].a_json())

    # Resumen del analizador
    print("\n" + "=" * 60)
    print("RESUMEN DEL ANALIZADOR:")
    resumen = AnalizadorTrazas.resumir(agente.historial_trazas)
    print(json.dumps(resumen, indent=2, ensure_ascii=False))
