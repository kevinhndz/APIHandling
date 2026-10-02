import sys
from pathlib import Path

# Agregar la raiz del proyecto al sys.path de Python automaticamente
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))