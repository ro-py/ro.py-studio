import os
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup

from .paths import StudioPaths
from .settings import Settings
from .storage import AppStorage

import orjson


class StudioClient:
    def __init__(self, path: Optional[Path] = None):
        if path is None:
            path = Path(os.getenv("LocalAppData")) / "Roblox"

        self.paths = StudioPaths(path)

    def get_settings(self) -> Settings:
        with open(self.paths.global_settings, "r") as file:
            soup = BeautifulSoup(
                markup=file.read(),
                features="lxml-xml"
            )
            return Settings(soup)

    def get_basic_settings(self) -> Settings:
        with open(self.paths.global_basic_settings, "r") as file:
            soup = BeautifulSoup(
                markup=file.read(),
                features="xml"
            )
            return Settings(soup)

    def get_cached_fflags(self) -> dict:
        with open(self.paths.studio_app_settings, "rb") as file:
            data = file.read()
            return orjson.loads(data)

    def get_app_storage(self):
        with open(self.paths.app_storage, "rb") as file:
            data = file.read()
            return AppStorage(orjson.loads(data))

