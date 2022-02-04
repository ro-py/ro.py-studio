import os
from pathlib import Path
from typing import Dict, Any, Optional

import aiofiles
import orjson

from .environments import Version, VersionType
from .paths import StudioPaths
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

        self.paths: StudioPaths = StudioPaths(roblox_path)

    def get_cached_fflags(self) -> Dict[str, Any]:
        with open(
            file=self.paths.studio_app_settings,
            mode="rb"
        ) as file:
            data = file.read()
        return orjson.loads(data)

    def get_app_storage(self):
        with aiofiles.open(
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
            paths=self.paths,
            version_type=version_type
        )
