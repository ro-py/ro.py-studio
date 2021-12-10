import asyncio
import os
import winreg
from pathlib import Path
from typing import List, Optional

import aiofiles
import orjson

from .environments import Environment, Version
from .paths import StudioPaths
from .registry import RobloxRegistry, RobloxCorpRegistry
from .settings import Settings
from .storage import AppStorage


class StudioClient:
    def __init__(
            self,
            roblox_path: Path = None,
            roblox_registry_location: str = None,
            roblox_corp_registry_location: str = None,
    ):
        if roblox_path is None:
            roblox_path = Path(os.getenv("LocalAppData")) / "Roblox"

        if roblox_registry_location is None:
            roblox_registry_location = r"SOFTWARE\Roblox"

        if roblox_corp_registry_location is None:
            roblox_corp_registry_location = r"SOFTWARE\ROBLOX Corporation"

        self.paths: StudioPaths = StudioPaths(roblox_path)
        self.registry: RobloxRegistry = RobloxRegistry(roblox_registry_location)
        self.corp_registry: RobloxCorpRegistry = RobloxCorpRegistry(roblox_corp_registry_location)

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

    def _get_environments(self):
        key = winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=self.corp_registry.environments,
            reserved=0,
            access=winreg.KEY_READ
        )
        item_index = 0
        sub_names = []

        while True:
            try:
                name, data, data_type = winreg.EnumValue(key, item_index)
                sub_names.append(name)
                item_index += 1
            except EnvironmentError:
                break

        environments = []

        for sub_name in sub_names:
            environment = Environment(
                name=sub_name,
                paths=self.paths
            )
            environment.load(self.corp_registry.environments + "\\" + sub_name)
            environments.append(environment)

        return environments

    async def get_environments(self) -> List[Environment]:
        return await asyncio.get_event_loop().run_in_executor(None, self._get_environments)

    async def get_studio_environment(self) -> Optional[Environment]:
        environments = await self.get_environments()
        for environment in environments:
            if environment.name == "roblox-studio":
                return environment
        return None

    def get_version(self, path: Path) -> Version:
        return Version(
            path=path,
            paths=self.paths
        )
