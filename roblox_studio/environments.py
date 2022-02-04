from enum import Enum
from pathlib import Path
from typing import Dict, Any

import aiofiles
import aiofiles.os

import orjson

from .paths import StudioPaths
from .settings import AppSettings


class VersionType(Enum):
    windows = "windows"
    """A Windows studio version.
    It contains the executable file (RobloxStudioBeta.exe) and is commonly located in %LocalAppData%/Roblox/Versions.
    """
    macos = "macos"
    """A macOS studio version.
    It should be an .app folder and contain a folder "Contents" with a file called "Info.plist".
    It is commonly located in ~/Applications."""


class Version:
    def __init__(self, path: Path, paths: StudioPaths, version_type: VersionType):
        self.path: Path = path
        self.version_type: VersionType = version_type
        self._paths: StudioPaths = paths

    @property
    def app_settings_file_path(self):
        return self._root_resources_path / "AppSettings.xml"

    @property
    def _root_resources_path(self):
        if self.version_type == VersionType.macos:
            return self.path / "Contents" / "Resources"
        else:
            return self.path

    @property
    def _root_executables_path(self):
        if self.version_type == VersionType.macos:
            return self.path / "Contents" / "MacOS"
        else:
            return self.path

    @property
    def content_folder_path(self):
        return self._root_resources_path / "content"

    @property
    def extra_content_folder_path(self):
        return self._root_resources_path / "ExtraContent"

    @property
    def platform_content_folder_path(self):
        return self._root_resources_path / "PlatformContent"

    @property
    def built_in_plugins_folder_path(self):
        return self._root_resources_path / "BuiltInPlugins"

    @property
    def built_in_standalone_plugins_folder_path(self):
        return self._root_resources_path / "BuiltInStandalonePlugins"

    @property
    def plugins_folder_path(self):
        return self._root_resources_path / "Plugins"

    @property
    def qml_folder_path(self):
        return self.path / "Qml"

    @property
    def shaders_folder_path(self):
        return self._root_resources_path / "shaders"

    @property
    def ssl_folder_path(self):
        return self._root_resources_path / "ssl"

    @property
    def cacert_file_path(self):
        return self.ssl_folder_path / "cacert.pem"

    @property
    def studio_fonts_folder_path(self):
        return self._root_resources_path / "StudioFonts"

    @property
    def client_settings_folder_path(self):
        return self._root_executables_path / "ClientSettings"

    @property
    def client_app_settings_file_path(self):
        return self.client_settings_folder_path / "ClientAppSettings.json"

    @property
    def reflection_metadata_file_path(self):
        return self._root_resources_path / "ReflectionMetadata.xml"

    @property
    def ribbon_file_path(self):
        return self._root_resources_path / "RobloxStudioRibbon.xml"

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
