"""
IL2.4: Buenas Practicas para Proyectos de Agentes de IA
========================================================
Demuestra patrones concretos: manejo de errores, configuracion con
variables de entorno, logica de reintento y validacion de entrada.

Ejecutar: python 2-best_practices.py
"""

import os
import time
import random
from dataclasses import dataclass
from typing import Optional


# --- Configuracion centralizada con variables de entorno ---

@dataclass
class Configuracion:
    """Carga y valida la configuracion desde variables de entorno."""
    api_base_url: str
    api_key: str
    modelo: str
    temperatura: float
    max_reintentos: int

    @classmethod
    def desde_entorno(cls) -> "Configuracion":
        """Crea configuracion desde variables de entorno con valores por defecto."""
        api_key = os.getenv("API_KEY", "demo-key-12345")
        if not api_key:
            raise ValueError("La variable API_KEY es obligatoria")
        return cls(
            api_base_url=os.getenv("API_BASE_URL", "https://api.example.com/v1"),
            api_key=api_key,
            modelo=os.getenv("MODELO_LLM", "gpt-4o-mini"),
            temperatura=float(os.getenv("TEMPERATURA", "0.7")),
            max_reintentos=int(os.getenv("MAX_REINTENTOS", "3")),
        )


# --- Validacion de entrada ---

def validar_mensaje(mensaje: str, largo_minimo: int = 1, largo_maximo: int = 2000) -> str:
    """Valida y limpia el mensaje de entrada del usuario."""
    if not isinstance(mensaje, str):
        raise TypeError(f"Se esperaba str, se recibio {type(mensaje).__name__}")
    mensaje = mensaje.strip()
    if len(mensaje) < largo_minimo:
        raise ValueError(f"El mensaje debe tener al menos {largo_minimo} caracter(es)")
    if len(mensaje) > largo_maximo:
        mensaje = mensaje[:largo_maximo]
    return mensaje


# --- Logica de reintento con backoff exponencial ---

class ErrorAPI(Exception):
    """Error personalizado para fallos de API."""
    def __init__(self, mensaje: str, codigo: int = 500):
        super().__init__(mensaje)
        self.codigo = codigo


def llamar_con_reintento(funcion, max_reintentos: int = 3,
                         base_espera: float = 0.1) -> str:
    """Ejecuta una funcion con reintentos y backoff exponencial."""
    ultimo_error = None
    for intento in range(1, max_reintentos + 1):
        try:
            return funcion()
        except ErrorAPI as e:
            ultimo_error = e
            if intento < max_reintentos:
                espera = base_espera * (2 ** (intento - 1))
                print(f"  [Reintento {intento}/{max_reintentos}] "
                      f"Error: {e} - Esperando {espera:.2f}s")
                time.sleep(espera)
    raise ErrorAPI(f"Fallo tras {max_reintentos} reintentos: {ultimo_error}")


# --- Simulacion de llamada a API con errores aleatorios ---

def simular_llamada_api(mensaje: str, config: Configuracion) -> str:
    """Simula una llamada a API que puede fallar aleatoriamente."""
    def _llamada():
        if random.random() < 0.4:  # 40% probabilidad de fallo
            raise ErrorAPI("Timeout del servidor", codigo=503)
        return f"[{config.modelo}] Respuesta para: {mensaje}"

    return llamar_con_reintento(_llamada, max_reintentos=config.max_reintentos)


# --- Manejo de errores estructurado ---

@dataclass
class ResultadoOperacion:
    """Encapsula el resultado de una operacion con manejo de errores."""
    exitoso: bool
    contenido: Optional[str] = None
    error: Optional[str] = None


def procesar_mensaje_seguro(mensaje: str, config: Configuracion) -> ResultadoOperacion:
    """Procesa un mensaje con manejo completo de errores."""
    try:
        mensaje_limpio = validar_mensaje(mensaje)
        respuesta = simular_llamada_api(mensaje_limpio, config)
        return ResultadoOperacion(exitoso=True, contenido=respuesta)
    except ValueError as e:
        return ResultadoOperacion(exitoso=False, error=f"Validacion: {e}")
    except TypeError as e:
        return ResultadoOperacion(exitoso=False, error=f"Tipo invalido: {e}")
    except ErrorAPI as e:
        return ResultadoOperacion(exitoso=False, error=f"API: {e}")


# --- Ejecucion de demostracion ---

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION: Buenas Practicas para Agentes de IA")
    print("=" * 60)

    # Cargar configuracion
    config = Configuracion.desde_entorno()
    print(f"\nConfiguracion cargada:")
    print(f"  Modelo: {config.modelo}")
    print(f"  URL base: {config.api_base_url}")
    print(f"  Reintentos: {config.max_reintentos}")

    # Pruebas con diferentes entradas
    print("\n--- Procesamiento de Mensajes ---")
    casos_prueba = [
        "Explica que es un agente de IA",
        "",          # vacio -> error de validacion
        "Consulta normal sobre LLMs",
        "   ",       # solo espacios -> error de validacion
    ]

    for caso in casos_prueba:
        print(f"\n  Entrada: {caso!r}")
        resultado = procesar_mensaje_seguro(caso, config)
        if resultado.exitoso:
            print(f"  Resultado: {resultado.contenido}")
        else:
            print(f"  Error: {resultado.error}")
