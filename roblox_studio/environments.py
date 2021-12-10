import asyncio
import winreg
from typing import Optional, Dict, Any
from pathlib import Path

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


class Environment(Version):
    def __init__(self, name: str = None, paths: StudioPaths = None):
        self._paths: StudioPaths = paths
        self.name: Optional[str] = name

        self.bootstrapper_path: Optional[str] = None
        self.channel: Optional[str] = None

        self.current_player_url: Optional[str] = None
        self.current_player_version: Optional[str] = None

        self.current_qt_studio_url: Optional[str] = None
        self.current_qt_studio_version: Optional[str] = None

        self.protocol_handler_scheme: Optional[str] = None
        self.version: Optional[str] = None
        self._key_path: Optional[str] = None

        super().__init__(
            path=self.get_version_path(),
            paths=self._paths
        )

    def load(self, key_path):
        self._key_path = key_path

        key = winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=key_path,
            reserved=0,
            access=winreg.KEY_READ
        )

        self.bootstrapper_path = soft_query(winreg.HKEY_CURRENT_USER, key_path)

        self.channel, _ = soft_query_ex(key, "channel")

        self.current_player_url, _ = soft_query_ex(key, "curPlayerUrl")
        self.current_player_version, _ = soft_query_ex(key, "curPlayerVer")

        self.current_qt_studio_url, _ = soft_query_ex(key, "curQTStudioUrl")
        self.current_qt_studio_version, _ = soft_query_ex(key, "curQTStudioVer")

        self.protocol_handler_scheme, _ = soft_query_ex(key, "protocol handler scheme")
        self.version, _ = soft_query_ex(key, "version")

        key.Close()

    def get_version_path(self):
        return self._paths.versions / self.version

    def _save(self):
        """
        Saves this environment to the registry.
        """
        key = winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=self._key_path,
            reserved=0,
            access=winreg.KEY_SET_VALUE
        )

        winreg.SetValue(winreg.HKEY_CURRENT_USER, self._key_path, winreg.REG_SZ, self.bootstrapper_path)

        soft_set_ex(key, "channel", winreg.REG_SZ, self.channel)

        soft_set_ex(key, "curPlayerUrl", winreg.REG_SZ, self.current_player_url)
        soft_set_ex(key, "curPlayerVer", winreg.REG_SZ, self.current_player_version)

        soft_set_ex(key, "curQTStudioUrl", winreg.REG_SZ, self.current_qt_studio_url)
        soft_set_ex(key, "curQTStudioVer", winreg.REG_SZ, self.current_qt_studio_version)

        soft_set_ex(key, "protocol handler scheme", winreg.REG_SZ, self.protocol_handler_scheme)
        soft_set_ex(key, "version", winreg.REG_SZ, self.version)

        key.Close()

    async def save(self):
        await asyncio.get_event_loop().run_in_executor(None, self._save)
