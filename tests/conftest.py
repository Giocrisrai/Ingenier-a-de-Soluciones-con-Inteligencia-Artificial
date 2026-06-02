import sys
from pathlib import Path

# Permite a los tests importar los módulos del backend con imports planos.
BACKEND_DIR = Path(__file__).resolve().parent.parent / "deploy" / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
