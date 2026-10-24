import sys
from pathlib import Path

# Makes `payment_integration` importable even when pytest is run from an IDE,
# from another folder, or with a pytest version that ignores `pythonpath`.
SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
