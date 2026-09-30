#!/usr/bin/env python3
"""Ejecuta de punta a punta los notebooks y scripts del curso contra Groq.

Uso:
    uv run python scripts/e2e.py                 # todo el repositorio
    uv run python scripts/e2e.py RA2/IL2.1       # solo una carpeta (o archivos sueltos)

Gasta cuota real de Groq (cada notebook hace llamadas al LLM), por eso NO corre en CI:
ejecutarlo completo consume una parte importante de la cuota diaria gratuita.

Los notebooks se ejecutan sobre una copia temporal, así que las salidas guardadas en el
repositorio no cambian. Además de las excepciones, se marca como fallo cualquier error que
un notebook capture y solo imprima (p. ej. un 429 de Groq dentro de un try/except).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import warnings
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

RAIZ = Path(__file__).resolve().parent.parent
TIMEOUT_CELDA = 600
TIMEOUT_SCRIPT = 600

# Módulos de apoyo o piezas que no se ejecutan sueltas (deploy/ tiene su propia CI).
EXCLUIDOS = {"scripts/", "tests/", "deploy/", "RA2/IL2.3/_demo_utils.py"}
APPS_STREAMLIT = {"RA1/IL1.3/2-text-chunking.py", "RA1/IL1.4/1-evaluation-rag.py"}

# Mensajes que solo aparecen ante un error real de la API o de Python. Los nombres de
# excepción sueltos no bastan: hay notebooks que los escriben en logs de ejemplo.
ERRORES_OCULTOS = re.compile(
    r"Rate limit reached|rate_limit_exceeded|Error code: [45]\d\d|GroqException"
    r"|invalid_request_error|Traceback \(most recent call last\)"
)


def rel(ruta: Path) -> str:
    return ruta.relative_to(RAIZ).as_posix()


def objetivos(filtros: list[str]) -> list[Path]:
    salida = subprocess.check_output(["git", "ls-files", "*.ipynb", "*.py"], cwd=RAIZ, text=True)
    rutas = [RAIZ / linea for linea in salida.splitlines()]
    rutas = [r for r in rutas if not any(rel(r).startswith(e) for e in EXCLUIDOS)]
    if filtros:
        rutas = [r for r in rutas if any(rel(r).startswith(f.rstrip("/")) for f in filtros)]
    return sorted(rutas)


def texto_de_salidas(nb: nbformat.NotebookNode) -> str:
    partes = []
    for celda in nb.cells:
        for salida in celda.get("outputs", []):
            partes.append("".join(salida.get("text", "")))
            partes.append("".join(salida.get("data", {}).get("text/plain", "")))
            partes.extend(salida.get("traceback", []))
    return "\n".join(partes)


def ejecutar_notebook(ruta: Path) -> str | None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        nb = nbformat.read(ruta, as_version=4)
    cliente = NotebookClient(
        nb,
        timeout=TIMEOUT_CELDA,
        kernel_name="python3",
        resources={"metadata": {"path": str(ruta.parent)}},
    )
    try:
        cliente.execute()
    except CellExecutionError as e:
        return str(e).strip().splitlines()[-1][:300]
    finally:
        destino = Path(tempfile.gettempdir()) / "e2e" / rel(ruta)
        destino.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(nb, destino)
    if m := ERRORES_OCULTOS.search(texto_de_salidas(nb)):
        return f"error capturado en las salidas: {m.group(0)} (ver {destino})"
    return None


def ejecutar_script(ruta: Path) -> str | None:
    entorno = {**os.environ, "MPLBACKEND": "Agg", "PYTHONUNBUFFERED": "1"}
    try:
        proc = subprocess.run(
            [sys.executable, ruta.name],
            cwd=ruta.parent,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SCRIPT,
            env=entorno,
        )
    except subprocess.TimeoutExpired:
        return f"superó {TIMEOUT_SCRIPT}s"
    salida = proc.stdout + proc.stderr
    if proc.returncode != 0:
        return (salida.strip().splitlines() or ["(sin salida)"])[-1][:300]
    if m := ERRORES_OCULTOS.search(salida):
        return f"error capturado en la salida: {m.group(0)}"
    return None


def ejecutar_streamlit(ruta: Path) -> str | None:
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(ruta), default_timeout=120)
    app.run()
    if app.exception:
        return app.exception[0].message[:300]
    return None


def main() -> int:
    rutas = objetivos(sys.argv[1:])
    fallos: dict[str, str] = {}
    for ruta in rutas:
        nombre = rel(ruta)
        inicio = time.monotonic()
        if ruta.suffix == ".ipynb":
            error = ejecutar_notebook(ruta)
        elif nombre in APPS_STREAMLIT:
            error = ejecutar_streamlit(ruta)
        else:
            error = ejecutar_script(ruta)
        estado = "OK   " if error is None else "FALLA"
        print(f"{estado} {time.monotonic() - inicio:6.1f}s  {nombre}", flush=True)
        if error:
            print(f"             {error}", flush=True)
            fallos[nombre] = error

    print(f"\n{len(rutas) - len(fallos)}/{len(rutas)} OK")
    (Path(tempfile.gettempdir()) / "e2e" / "resumen.json").write_text(
        json.dumps(fallos, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
