from pathlib import Path
from typing import Dict, Any

import aiofiles
import aiofiles.os

import orjson

from .paths import StudioPaths
from .settings import AppSettings


class Version:
    def __init__(self, path: Path, paths: StudioPaths):
        self.path: Path = path
        self._paths: StudioPaths = paths

    @property
    def app_settings_file_path(self):
        return self.path / "AppSettings.xml"

    @property
    def content_folder_path(self):
        return self.path / "content"

    @property
    def extra_content_folder_path(self):
        return self.path / "ExtraContent"

    @property
    def platform_content_folder_path(self):
        return self.path / "PlatformContent"

    @property
    def built_in_plugins_folder_path(self):
        return self.path / "BuiltInPlugins"

    @property
    def built_in_standalone_plugins_folder_path(self):
        return self.path / "BuiltInStandalonePlugins"

    @property
    def plugins_folder_path(self):
        return self.path / "Plugins"

    @property
    def qml_folder_path(self):
        return self.path / "Qml"

    @property
    def shaders_folder_path(self):
        return self.path / "shaders"

    @property
    def ssl_folder_path(self):
        return self.path / "ssl"

    @property
    def cacert_file_path(self):
        return self.ssl_folder_path / "cacert.pem"

    @property
    def studio_fonts_folder_path(self):
        return self.path / "StudioFonts"

    @property
    def client_settings_folder_path(self):
        return self.path / "ClientSettings"

    @property
    def client_app_settings_file_path(self):
        return self.client_settings_folder_path / "ClientAppSettings.json"

    async def get_app_settings(self):
        async with aiofiles.open(
                file=self.app_settings_file_path,
                mode="r"
        ) as file:
            data = await file.read()
        app_settings = AppSettings(self.path)
        await app_settings.from_xml(data)
        return app_settings

    async def get_fflag_overrides(self) -> Dict[str, Any]:
        try:
            async with aiofiles.open(self.client_app_settings_file_path, "rb") as client_app_settings_file:
                fflag_overrides_json = await client_app_settings_file.read()

            return orjson.loads(fflag_overrides_json)
        except FileNotFoundError:
            return {}

    async def set_fflag_overrides(self, overrides: Dict[str, Any]):
        try:
            await aiofiles.os.mkdir(self.client_settings_folder_path)
        except FileExistsError:
            pass

        fflag_overrides_json = orjson.dumps(overrides)

        async with aiofiles.open(self.client_app_settings_file_path, "wb") \
                as client_app_settings_file:
            await client_app_settings_file.write(fflag_overrides_json)
