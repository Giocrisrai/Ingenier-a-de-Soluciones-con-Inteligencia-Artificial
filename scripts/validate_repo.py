#!/usr/bin/env python3
"""Validaciones estáticas del repositorio (usar con: uv run python scripts/validate_repo.py [--fix]).

Comprueba, sin llamar a ningún LLM:
  1. Que todos los notebooks cumplan el esquema nbformat (si no, nbconvert y Colab fallan).
  2. Que no queden referencias al proveedor retirado (GitHub Models), ver CLAUDE.md.
  3. Que requirements.txt pida exactamente lo mismo que pyproject.toml.
  4. Que todos los scripts .py compilen.

Con --fix normaliza los notebooks inválidos: nbformat 4.5, ids de celda y los campos
obligatorios que algunos editores borran al guardar (`name` en stream, `metadata` en
display_data/execute_result).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
import uuid
import warnings
from pathlib import Path

import nbformat
from packaging.requirements import Requirement

RAIZ = Path(__file__).resolve().parent.parent

REFERENCIAS_PROHIBIDAS = re.compile(
    r"GITHUB_TOKEN|GITHUB_BASE_URL|OPENAI_BASE_URL|models\.inference\.ai\.azure\.com|gpt-4o"
)
# Archivos que nombran esas referencias a propósito: las reglas que las prohíben y el
# plan histórico de IL3.5, que lleva un aviso de obsolescencia con la equivalencia actual.
EXCEPCIONES = {
    "CLAUDE.md",
    "GEMINI.md",
    "scripts/validate_repo.py",
    "docs/superpowers/plans/2026-06-02-il3.5-ciberseguridad-despliegue-aws.md",
}


def archivos_versionados(*patrones: str) -> list[Path]:
    salida = subprocess.check_output(["git", "ls-files", *patrones], cwd=RAIZ, text=True)
    return [RAIZ / linea for linea in salida.splitlines() if linea]


def normalizar_notebook(nb: nbformat.NotebookNode) -> None:
    nb.nbformat, nb.nbformat_minor = 4, 5
    for celda in nb.cells:
        celda.setdefault("id", uuid.uuid4().hex[:12])
        celda.setdefault("metadata", {})
        if celda.cell_type == "code":
            celda.setdefault("execution_count", None)
            celda.setdefault("outputs", [])
        for salida in celda.get("outputs", []):
            tipo = salida.get("output_type")
            if tipo == "stream":
                salida.setdefault("name", "stdout")
            elif tipo in ("display_data", "execute_result"):
                salida.setdefault("metadata", {})
                if tipo == "execute_result":
                    salida.setdefault("execution_count", None)


def validar_notebooks(corregir: bool) -> list[str]:
    errores = []
    for ruta in archivos_versionados("*.ipynb"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nb = nbformat.read(ruta, as_version=4)
            try:
                nbformat.validate(nb)
                continue
            except nbformat.ValidationError as e:
                if not corregir:
                    errores.append(f"{ruta.relative_to(RAIZ)}: {e.message}")
                    continue
            # Solo se reescriben los inválidos, para no generar diffs de formato en el resto.
            normalizar_notebook(nb)
            try:
                nbformat.validate(nb)
            except nbformat.ValidationError as e:
                errores.append(f"{ruta.relative_to(RAIZ)}: {e.message}")
                continue
        nbformat.write(nb, ruta)
        print(f"         normalizado: {ruta.relative_to(RAIZ)}")
    return errores


def buscar_referencias_prohibidas() -> list[str]:
    errores = []
    for ruta in archivos_versionados():
        relativa = ruta.relative_to(RAIZ).as_posix()
        if relativa in EXCEPCIONES or not ruta.is_file():
            continue
        try:
            texto = ruta.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for n, linea in enumerate(texto.splitlines(), 1):
            if m := REFERENCIAS_PROHIBIDAS.search(linea):
                errores.append(f"{relativa}:{n}: {m.group(0)}")
    return errores


def comparar_requirements() -> list[str]:
    """requirements.txt es el respaldo para pip: debe pedir lo mismo que pyproject.toml."""
    proyecto = tomllib.loads((RAIZ / "pyproject.toml").read_text(encoding="utf-8"))
    esperadas = {Requirement(d).name.lower(): Requirement(d) for d in proyecto["project"]["dependencies"]}
    declaradas = {}
    for linea in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines():
        if linea := linea.split("#")[0].strip():
            req = Requirement(linea)
            declaradas[req.name.lower()] = req
    errores = [f"falta en requirements.txt: {esperadas[n]}" for n in esperadas.keys() - declaradas.keys()]
    errores += [f"sobra en requirements.txt: {declaradas[n]}" for n in declaradas.keys() - esperadas.keys()]
    errores += [
        f"distinto: pyproject pide {esperadas[n]} y requirements.txt {declaradas[n]}"
        for n in esperadas.keys() & declaradas.keys()
        if str(esperadas[n]) != str(declaradas[n])
    ]
    return sorted(errores)


def compilar_scripts() -> list[str]:
    errores = []
    for ruta in archivos_versionados("*.py"):
        try:
            compile(ruta.read_text(encoding="utf-8"), str(ruta), "exec")
        except SyntaxError as e:
            errores.append(f"{ruta.relative_to(RAIZ)}:{e.lineno}: {e.msg}")
    return errores


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fix", action="store_true", help="normaliza el formato de los notebooks")
    args = parser.parse_args()

    comprobaciones = [
        ("Notebooks (esquema nbformat)", validar_notebooks(args.fix)),
        ("Referencias a GitHub Models", buscar_referencias_prohibidas()),
        ("requirements.txt alineado con pyproject.toml", comparar_requirements()),
        ("Scripts .py compilan", compilar_scripts()),
    ]
    fallos = 0
    for nombre, errores in comprobaciones:
        print(f"{'OK   ' if not errores else 'ERROR'}  {nombre}")
        for error in errores:
            print(f"         {error}")
        fallos += len(errores)

    if fallos:
        print(f"\n{fallos} problema(s). Para el formato de notebooks: uv run python scripts/validate_repo.py --fix")
        return 1
    print("\nListo: repositorio validado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
