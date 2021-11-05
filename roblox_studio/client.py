import os
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup

from .paths import StudioPaths
from .settings import StudioSettings


class StudioClient:
    def __init__(self, path: Optional[Path] = None):
        if path is None:
            path = Path(os.getenv("LocalAppData")) / "Roblox"

        self.paths = StudioPaths(path)

    def get_settings(self):
        with open(self.paths.global_settings, "r") as file:
            soup = BeautifulSoup(
                markup=file.read(),
                features="lxml"
            )
            return StudioSettings(soup)
