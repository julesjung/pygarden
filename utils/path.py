from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_DIR = Path(sys.executable).resolve().parent