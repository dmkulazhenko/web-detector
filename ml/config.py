import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()


DETECTRON_MODEL_CFG = os.getenv(
    "DETECTRON_MODEL_CFG",
    str(BASE_DIR / "models" / "test.yaml")
)
DETECTRON_MODEL_TS = 0.5
