from enum import Enum
from pathlib import Path
from typing import Dict, Any

import os
import orjson
import subprocess


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
    def __init__(self, path: Path, version_type: VersionType):
        self.path: Path = path
        self.version_type: VersionType = version_type

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

    @property
    def binary_file_path(self):
        if self.version_type == VersionType.macos:
            return self._root_executables_path / "RobloxStudio"
        else:
            return self._root_resources_path / "RobloxStudioBeta.exe"

    def get_fflag_overrides(self) -> Dict[str, Any]:
        """
        Gets the active FFlag overrides for this Studio version.
        If no overrides have been set, an empty dictionary is returned.
        """

        try:
            with open(
                    file=self.client_app_settings_file_path,
                    mode="rb"
            ) as client_app_settings_file:
                data = client_app_settings_file.read()

            return orjson.loads(data)
        except FileNotFoundError:
            return {}

    def set_fflag_overrides(self, overrides: Dict[str, Any]):
        """
        Sets the FFlag overrides for this Studio version.
        """

        try:
            os.mkdir(self.client_settings_folder_path)
        except FileExistsError:
            pass

        fflag_overrides_json = orjson.dumps(overrides)

        with open(
            file=self.client_app_settings_file_path,
            mode="wb"
        ) as client_app_settings_file:
            client_app_settings_file.write(fflag_overrides_json)

    def generate_api_dump_to_path(self, path: Path):
        """
        Generates an API dump for this Roblox Studio version and places it in the specified path.
        """

        return subprocess.run(
            args=[
                self.binary_file_path, "-API", str(path)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
