"""Utilidades pequeñas para ejecutar demos educativas."""

import sys


def pause_demo(message: str) -> None:
    """Pausa solo cuando la demo se ejecuta en una terminal interactiva."""
    if sys.stdin.isatty():
        input(message)
    else:
        print(f"{message} [continuando automáticamente]")
