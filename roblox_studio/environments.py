import os

if os.name == "nt":
    import winreg

from pathlib import Path
from typing import Dict, Any

import aiofiles
import aiofiles.os
import orjson

from .paths import StudioPaths
from .settings import AppSettings


def soft_query(key, name):
    try:
        return winreg.QueryValue(key, name)
    except FileNotFoundError:
        return None


def soft_query_ex(key, name):
    try:
        value, value_type = winreg.QueryValueEx(key, name)
        return value, value_type
    except FileNotFoundError:
        return None, None


def soft_set_ex(key, name, type, value):
    if value is not None:
        winreg.SetValueEx(key, name, 0, type, value)


class Version:
    def __init__(self, path: Path, paths: StudioPaths):
        self._path: Path = path
        self._paths: StudioPaths = paths

    def get_app_settings_path(self):
        return self._path / "AppSettings.xml"

    async def get_app_settings(self):
        async with aiofiles.open(
                file=self.get_app_settings_path(),
                mode="r"
        ) as file:
            data = await file.read()
        app_settings = AppSettings(self._path)
        await app_settings.from_xml(data)
        return app_settings

    async def get_fflag_overrides(self) -> Dict[str, Any]:
        try:
            client_settings_path = self._path / "ClientSettings"

            async with aiofiles.open(client_settings_path / "ClientAppSettings.json", "rb") as client_app_settings_file:
                fflag_overrides_json = await client_app_settings_file.read()

            fflag_overrides = orjson.loads(fflag_overrides_json)
            return fflag_overrides
        except FileNotFoundError:
            return {}

    async def set_fflag_overrides(self, fflag_overrides: Dict[str, Any]):
        client_settings_path = self._path / "ClientSettings"
        try:
            await aiofiles.os.mkdir(client_settings_path)
        except FileExistsError:
            pass

        fflag_overrides_json = orjson.dumps(fflag_overrides)

        async with aiofiles.open(client_settings_path / "ClientAppSettings.json", "wb") as client_app_settings_file:
            await client_app_settings_file.write(fflag_overrides_json)
