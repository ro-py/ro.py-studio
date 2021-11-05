import os
from pathlib import Path
from typing import Optional

from .paths import StudioPaths


class StudioClient:
    def __init__(self, path: Optional[Path] = None):
        if path is None:
            path = Path(os.getenv("LocalAppData")) / "Roblox"

        self.path = path

        self.paths = StudioPaths(path)
