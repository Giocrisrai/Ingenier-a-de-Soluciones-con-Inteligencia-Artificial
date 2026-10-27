import sys
from pathlib import Path

# Los tests de esta carpeta importan `cargar` como módulo hermano.
sys.path.insert(0, str(Path(__file__).resolve().parent))
