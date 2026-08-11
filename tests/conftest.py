import os
import sys
from pathlib import Path

# Permite a los tests importar los módulos del backend con imports planos.
BACKEND_DIR = Path(__file__).resolve().parent.parent / "deploy" / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# El backend crea su AgentClient al importar app.py: si la máquina que corre los
# tests tiene una GROQ_API_KEY real en el entorno, el agente saldría de modo demo
# e intentaría llamar a Groq. Se limpia antes de importar nada del backend para
# que la suite sea determinista y no gaste cuota.
os.environ.pop("GROQ_API_KEY", None)
