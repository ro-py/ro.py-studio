from typing import Optional, Dict, Any

import orjson
import winreg
import aiofiles
import aiofiles.os

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


class Environment:
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

    def load(self, key_path):
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

    def get_version_path(self):
        return self._paths.versions / self.version

    def get_app_settings_path(self):
        return self.get_version_path() / "AppSettings.xml"

    async def get_app_settings(self):
        async with aiofiles.open(
                file=self.get_app_settings_path(),
                mode="r"
        ) as file:
            data = await file.read()
        app_settings = AppSettings(self.get_version_path())
        await app_settings.from_xml(data)
        return app_settings

    async def set_fflag_overrides(self, fflag_overrides: Dict[str, Any]):
        client_settings_path = self.get_version_path() / "ClientSettings"
        try:
            await aiofiles.os.mkdir(client_settings_path)
        except FileExistsError:
            pass

        fflag_overrides_json = orjson.dumps(fflag_overrides)

        async with aiofiles.open(client_settings_path / "ClientAppSettings.json", "wb") as client_app_settings_file:
            await client_app_settings_file.write(fflag_overrides_json)
