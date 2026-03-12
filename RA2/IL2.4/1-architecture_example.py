"""
IL2.4: Ejemplo de Arquitectura Limpia para Agentes de IA
=========================================================
Demuestra separacion clara de capas (presentacion, aplicacion, dominio,
infraestructura) con un agente que enruta herramientas de forma segura
sin usar eval().

Ejecutar: python 1-architecture_example.py
"""

import ast
import re
from typing import Callable, Dict, Optional
from dataclasses import dataclass


# =====================================================
# CAPA DE DOMINIO - Logica de negocio pura
# =====================================================

@dataclass
class Respuesta:
    """Modelo de dominio para la respuesta del agente."""
    contenido: str
    herramienta_usada: Optional[str] = None
    exitoso: bool = True


# --- Herramientas del dominio ---

def calculadora(expresion: str) -> str:
    """Evalua expresiones matematicas de forma segura usando AST."""
    try:
        arbol = ast.parse(expresion.strip(), mode="eval")
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                 ast.Constant, ast.Add, ast.Sub, ast.Mult,
                                 ast.Div, ast.Pow, ast.Mod, ast.USub)):
                continue
            return f"Error: operacion no permitida ({type(nodo).__name__})"
        resultado = eval(compile(arbol, "<entrada>", "eval"))
        return f"Resultado: {resultado}"
    except (SyntaxError, ZeroDivisionError) as e:
        return f"Error de calculo: {e}"


def buscador(consulta: str) -> str:
    """Simula una busqueda en base de conocimiento."""
    conocimiento = {
        "python": "Python es un lenguaje de programacion de alto nivel.",
        "ia": "La inteligencia artificial busca simular capacidades cognitivas.",
        "llm": "Los LLM son modelos de lenguaje entrenados con grandes corpus de texto.",
        "langchain": "LangChain es un framework para construir aplicaciones con LLMs.",
    }
    consulta_lower = consulta.lower()
    for clave, valor in conocimiento.items():
        if clave in consulta_lower:
            return valor
    return "No se encontro informacion sobre esa consulta."


def traductor(texto: str) -> str:
    """Simula traduccion basica espanol-ingles."""
    traducciones = {
        "hola": "hello", "mundo": "world", "agente": "agent",
        "inteligencia artificial": "artificial intelligence",
    }
    texto_lower = texto.lower()
    for esp, eng in traducciones.items():
        texto_lower = texto_lower.replace(esp, eng)
    return f"Traduccion: {texto_lower}"


# =====================================================
# CAPA DE INFRAESTRUCTURA - Registro de herramientas
# =====================================================

class RegistroHerramientas:
    """Registra y gestiona las herramientas disponibles para el agente."""

    def __init__(self):
        self._herramientas: Dict[str, Callable] = {}
        self._descripciones: Dict[str, str] = {}

    def registrar(self, nombre: str, funcion: Callable, descripcion: str):
        self._herramientas[nombre] = funcion
        self._descripciones[nombre] = descripcion

    def obtener(self, nombre: str) -> Optional[Callable]:
        return self._herramientas.get(nombre)

    def listar(self) -> Dict[str, str]:
        return dict(self._descripciones)


# =====================================================
# CAPA DE APLICACION - Orquestacion del agente
# =====================================================

class AgenteOrquestador:
    """Orquesta la logica del agente: clasifica intencion y enruta a herramientas."""

    # Mapeo de palabras clave a herramientas
    REGLAS_ENRUTAMIENTO = {
        "calculadora": ["suma", "resta", "calcula", "cuanto es", "multiplica", "+", "-", "*", "/"],
        "buscador": ["que es", "busca", "explica", "define", "informacion"],
        "traductor": ["traduce", "traduccion", "en ingles", "translate"],
    }

    def __init__(self, registro: RegistroHerramientas):
        self.registro = registro

    def clasificar_intencion(self, mensaje: str) -> Optional[str]:
        """Determina que herramienta usar segun el contenido del mensaje."""
        mensaje_lower = mensaje.lower()
        for herramienta, palabras_clave in self.REGLAS_ENRUTAMIENTO.items():
            if any(clave in mensaje_lower for clave in palabras_clave):
                return herramienta
        return None

    def _extraer_entrada(self, mensaje: str, herramienta: str) -> str:
        """Extrae la entrada relevante del mensaje segun la herramienta."""
        if herramienta == "calculadora":
            # Extraer la expresion matematica del mensaje
            expresion = re.findall(r"[\d\s\+\-\*\/\(\)\.\^]+", mensaje)
            if expresion:
                # Tomar la coincidencia mas larga que contenga digitos
                candidatas = [e.strip() for e in expresion if re.search(r"\d", e)]
                if candidatas:
                    return max(candidatas, key=len)
            return mensaje
        return mensaje

    def procesar(self, mensaje: str) -> Respuesta:
        """Procesa un mensaje: clasifica, enruta y ejecuta."""
        nombre_herramienta = self.clasificar_intencion(mensaje)

        if nombre_herramienta is None:
            return Respuesta(
                contenido="No tengo una herramienta adecuada para esa consulta.",
                exitoso=False,
            )

        funcion = self.registro.obtener(nombre_herramienta)
        if funcion is None:
            return Respuesta(
                contenido=f"Herramienta '{nombre_herramienta}' no disponible.",
                exitoso=False,
            )

        entrada = self._extraer_entrada(mensaje, nombre_herramienta)
        resultado = funcion(entrada)
        return Respuesta(
            contenido=resultado,
            herramienta_usada=nombre_herramienta,
            exitoso=True,
        )


# =====================================================
# CAPA DE PRESENTACION - Interfaz de usuario
# =====================================================

def mostrar_respuesta(mensaje: str, respuesta: Respuesta):
    """Muestra la respuesta formateada al usuario."""
    estado = "OK" if respuesta.exitoso else "SIN HERRAMIENTA"
    herramienta = respuesta.herramienta_usada or "ninguna"
    print(f"  [{estado}] Herramienta: {herramienta}")
    print(f"  Entrada:   {mensaje}")
    print(f"  Respuesta: {respuesta.contenido}")
    print()


# --- Ejecucion de demostracion ---

if __name__ == "__main__":
    # Configurar infraestructura
    registro = RegistroHerramientas()
    registro.registrar("calculadora", calculadora, "Evalua expresiones matematicas")
    registro.registrar("buscador", buscador, "Busca en base de conocimiento")
    registro.registrar("traductor", traductor, "Traduce texto al ingles")

    # Crear agente
    agente = AgenteOrquestador(registro)

    print("=" * 60)
    print("DEMOSTRACION: Arquitectura Limpia para Agentes de IA")
    print("=" * 60)

    # Mostrar herramientas disponibles
    print("\nHerramientas registradas:")
    for nombre, desc in registro.listar().items():
        print(f"  - {nombre}: {desc}")
    print()

    # Procesar mensajes de prueba
    mensajes = [
        "Calcula cuanto es 15 * 7 + 3",
        "Que es un LLM",
        "Traduce inteligencia artificial en ingles",
        "Cual es el clima hoy",  # sin herramienta disponible
        "Busca informacion sobre Python",
    ]

    for msg in mensajes:
        respuesta = agente.procesar(msg)
        mostrar_respuesta(msg, respuesta)
