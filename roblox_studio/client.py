import os
from pathlib import Path
from typing import Dict, Any

import aiofiles
import orjson

from .environments import Version
from .paths import StudioPaths
from .settings import Settings
from .storage import AppStorage


class StudioClient:
    def __init__(
            self,
            roblox_path: Path = None,
    ):
        if roblox_path is None:
            if os.name == "nt":
                roblox_path = Path(os.getenv("LocalAppData")) / "Roblox"
            else:
                roblox_path = Path("~/Library").expanduser() / "Roblox"

        self.paths: StudioPaths = StudioPaths(roblox_path)

    async def get_settings(self) -> Settings:
        async with aiofiles.open(
                file=self.paths.global_settings,
                mode="r"
        ) as file:
            markup = await file.read()

        settings = Settings()
        await settings.from_xml(markup)
        return settings

    async def get_basic_settings(self) -> Settings:
        async with aiofiles.open(
                file=self.paths.global_basic_settings,
                mode="r"
        ) as file:
            markup = await file.read()

        settings = Settings()
        await settings.from_xml(markup)
        return settings

    async def get_cached_fflags(self) -> Dict[str, Any]:
        async with aiofiles.open(
                file=self.paths.studio_app_settings,
                mode="rb"
        ) as file:
            data = await file.read()
        return orjson.loads(data)

    async def get_app_storage(self):
        async with aiofiles.open(
                file=self.paths.app_storage,
                mode="rb"
        ) as file:
            data = await file.read()
        return AppStorage(orjson.loads(data))

    def get_version(self, path: Path) -> Version:
        return Version(
            path=path,
            paths=self.paths
        )
