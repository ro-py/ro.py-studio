import os
from pathlib import Path
from bs4 import BeautifulSoup

from .paths import StudioPaths
from .settings import Settings
from .storage import AppStorage
from .registry import RobloxRegistryPaths, RobloxCorpRegistryPaths

import orjson
import aiofiles


class StudioClient:
    def __init__(
            self,
            roblox_path: Path = None,
            roblox_registry_location: str = None,
            roblox_corp_registry_location: str = None,
    ):
        if roblox_path is None:
            roblox_path = Path(os.getenv("LocalAppData")) / "Roblox"

        if roblox_registry_location:
            roblox_registry_location = r"SOFTWARE\Roblox"

        if roblox_corp_registry_location is None:
            roblox_corp_registry_location = r"SOFTWARE\ROBLOX Corporation"

        self.paths = StudioPaths(roblox_path)
        self.registry_paths: RobloxRegistryPaths(roblox_registry_location)
        self.corp_registry_paths: RobloxCorpRegistryPaths(roblox_corp_registry_location)

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

    async def get_cached_fflags(self) -> dict:
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
