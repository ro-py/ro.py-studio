import os
from pathlib import Path
from typing import Dict, Any, Optional

import orjson

from .environments import Version, VersionType
from .storage import AppStorage

_is_windows = os.name == "nt"
_is_posix = os.name == "posix"


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

        self.path: Path = roblox_path

    @property
    def global_settings_file_path(self):
        return self.path / "GlobalSettings_13.xml"

    @property
    def global_basic_settings_file_path(self):
        return self.path / "GlobalBasicSettings_13.xml"

    @property
    def analystics_settings_file_path(self):
        return self.path / "AnalysticsSettings.xml"

    @property
    def client_settings_folder_path(self):
        return self.path / "ClientSettings"

    @property
    def studio_app_settings_file_path(self):
        return self.client_settings_folder_path / "StudioAppSettings.json"

    def get_cached_fflags(self) -> Dict[str, Any]:
        with open(
                file=self.paths.studio_app_settings,
                mode="rb"
        ) as file:
            data = file.read()
        return orjson.loads(data)

    def get_app_storage(self):
        with open(
                file=self.paths.app_storage,
                mode="rb"
        ) as file:
            data = file.read()
        return AppStorage(orjson.loads(data))

    def get_version(self, path: Path, version_type: Optional[VersionType] = None) -> Version:
        if version_type is None:
            if _is_windows:
                version_type = VersionType.windows
            elif _is_posix:
                version_type = VersionType.macos
            else:
                raise Exception("Couldn't determine your OS type. Specify the version_type parameter to silence this.")

        return Version(
            path=path,
            version_type=version_type
        )
