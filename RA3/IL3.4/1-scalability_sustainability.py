"""
IL3.4: Escalabilidad y Sostenibilidad
======================================
Demuestra un sistema de cache para respuestas LLM, procesamiento por lotes,
estimacion de uso de tokens y enrutamiento de modelos segun complejidad
para optimizacion de costos.

Ejecutar: python 1-scalability_sustainability.py
"""

import hashlib
import time
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict


# --- Cache de respuestas LLM ---

class CacheLLM:
    """Cache simple basado en hash del prompt para evitar llamadas repetidas."""

    def __init__(self, tamano_maximo: int = 100):
        self.cache: Dict[str, dict] = {}
        self.tamano_maximo = tamano_maximo
        self.aciertos = 0
        self.fallos = 0

    def _generar_clave(self, prompt: str, modelo: str) -> str:
        contenido = f"{modelo}:{prompt}"
        return hashlib.sha256(contenido.encode()).hexdigest()[:16]

    def obtener(self, prompt: str, modelo: str) -> Optional[str]:
        clave = self._generar_clave(prompt, modelo)
        if clave in self.cache:
            self.aciertos += 1
            return self.cache[clave]["respuesta"]
        self.fallos += 1
        return None

    def guardar(self, prompt: str, modelo: str, respuesta: str, tokens_usados: int):
        if len(self.cache) >= self.tamano_maximo:
            # Eliminar la entrada mas antigua (FIFO simple)
            clave_antigua = next(iter(self.cache))
            del self.cache[clave_antigua]
        clave = self._generar_clave(prompt, modelo)
        self.cache[clave] = {"respuesta": respuesta, "tokens": tokens_usados}

    def estadisticas(self) -> dict:
        total = self.aciertos + self.fallos
        return {
            "aciertos": self.aciertos,
            "fallos": self.fallos,
            "tasa_acierto_pct": round((self.aciertos / total) * 100, 1) if total else 0,
            "entradas_en_cache": len(self.cache),
        }


# --- Estimador de tokens ---

def estimar_tokens(texto: str) -> int:
    """Estimacion simple: ~1 token por cada 4 caracteres (aprox. para espanol)."""
    return max(1, len(texto) // 4)


# --- Enrutador de modelos segun complejidad ---

@dataclass
class ConfigModelo:
    nombre: str
    costo_por_1k_tokens: float  # USD
    latencia_promedio_ms: float
    capacidad_maxima_tokens: int


MODELOS_DISPONIBLES = {
    "rapido": ConfigModelo("gpt-4o-mini", 0.00015, 200, 4096),
    "estandar": ConfigModelo("gpt-4o", 0.005, 800, 8192),
    "avanzado": ConfigModelo("o1", 0.015, 2000, 16384),
}


def clasificar_complejidad(prompt: str) -> str:
    """Clasifica la complejidad de un prompt para enrutar al modelo adecuado."""
    tokens_estimados = estimar_tokens(prompt)
    palabras_complejas = ["analiza", "compara", "evalua", "arquitectura",
                          "estrategia", "optimiza", "multi-paso", "razonamiento"]
    indicadores_complejos = sum(1 for p in palabras_complejas if p in prompt.lower())

    if tokens_estimados > 200 or indicadores_complejos >= 2:
        return "avanzado"
    elif tokens_estimados > 50 or indicadores_complejos >= 1:
        return "estandar"
    return "rapido"


def seleccionar_modelo(prompt: str) -> ConfigModelo:
    """Selecciona el modelo mas eficiente segun la complejidad del prompt."""
    nivel = clasificar_complejidad(prompt)
    return MODELOS_DISPONIBLES[nivel]


# --- Procesamiento por lotes ---

@dataclass
class ResultadoLote:
    prompt: str
    respuesta: str
    modelo_usado: str
    tokens_usados: int
    desde_cache: bool
    costo_estimado_usd: float


def procesar_lote(prompts: List[str], cache: CacheLLM) -> List[ResultadoLote]:
    """Procesa un lote de prompts con cache y enrutamiento de modelos."""
    resultados = []

    for prompt in prompts:
        modelo = seleccionar_modelo(prompt)

        # Verificar cache
        respuesta_cache = cache.obtener(prompt, modelo.nombre)
        if respuesta_cache is not None:
            resultados.append(ResultadoLote(
                prompt=prompt[:50], respuesta=respuesta_cache[:50],
                modelo_usado=modelo.nombre, tokens_usados=0,
                desde_cache=True, costo_estimado_usd=0.0,
            ))
            continue

        # Simular llamada al modelo
        tokens_in = estimar_tokens(prompt)
        tokens_out = random.randint(20, 150)
        total_tokens = tokens_in + tokens_out
        costo = (total_tokens / 1000) * modelo.costo_por_1k_tokens
        respuesta = f"[{modelo.nombre}] Respuesta simulada para: {prompt[:30]}..."

        cache.guardar(prompt, modelo.nombre, respuesta, total_tokens)
        resultados.append(ResultadoLote(
            prompt=prompt[:50], respuesta=respuesta[:50],
            modelo_usado=modelo.nombre, tokens_usados=total_tokens,
            desde_cache=False, costo_estimado_usd=round(costo, 6),
        ))

    return resultados


# --- Ejecucion de demostracion ---

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION: Escalabilidad y Sostenibilidad")
    print("=" * 60)

    cache = CacheLLM(tamano_maximo=50)

    # Lote 1: prompts variados
    prompts_lote1 = [
        "Hola, que hora es",
        "Explica que es un LLM",
        "Analiza y compara las estrategias de escalabilidad para agentes multi-paso "
        "considerando arquitectura de microservicios y optimiza el rendimiento",
        "Traduce 'hola' al ingles",
        "Evalua la arquitectura propuesta y razona sobre sus ventajas",
    ]

    print("\n--- Lote 1: Procesamiento Inicial ---")
    resultados1 = procesar_lote(prompts_lote1, cache)
    costo_total = 0.0
    for r in resultados1:
        origen = "CACHE" if r.desde_cache else r.modelo_usado
        print(f"  [{origen}] {r.prompt[:45]}... -> {r.tokens_usados} tokens, ${r.costo_estimado_usd}")
        costo_total += r.costo_estimado_usd
    print(f"  Costo total lote 1: ${costo_total:.6f}")

    # Lote 2: algunos repetidos para demostrar el cache
    prompts_lote2 = [
        "Hola, que hora es",  # repetido
        "Explica que es un LLM",  # repetido
        "Genera un resumen ejecutivo del proyecto",  # nuevo
    ]

    print("\n--- Lote 2: Con Cache Activo ---")
    resultados2 = procesar_lote(prompts_lote2, cache)
    costo_total2 = 0.0
    for r in resultados2:
        origen = "CACHE" if r.desde_cache else r.modelo_usado
        print(f"  [{origen}] {r.prompt[:45]}... -> {r.tokens_usados} tokens, ${r.costo_estimado_usd}")
        costo_total2 += r.costo_estimado_usd
    print(f"  Costo total lote 2: ${costo_total2:.6f}")

    # Estadisticas del cache
    print("\n--- Estadisticas del Cache ---")
    stats = cache.estadisticas()
    for clave, valor in stats.items():
        print(f"  {clave}: {valor}")

    # Resumen de enrutamiento
    print("\n--- Enrutamiento de Modelos ---")
    for prompt in prompts_lote1:
        modelo = seleccionar_modelo(prompt)
        nivel = clasificar_complejidad(prompt)
        print(f"  [{nivel:>9}] {modelo.nombre:>12} -> {prompt[:50]}...")
