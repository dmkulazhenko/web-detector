import os
from pathlib import Path


class Config:
    VIDEO_STORAGE = Path(os.getenv("VIDEO_STORAGE", "~/storage")).absolute()
    CHUNK_SIZE = 10
