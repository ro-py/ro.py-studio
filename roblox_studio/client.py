import os
from pathlib import Path
from typing import Dict, Any, Optional

import orjson

from .environments import Version, VersionType
from .storage import AppStorage
from .cookie import RobloxCookie
from .settings import get_raw_settings

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

    @property
    def local_storage_folder_path(self):
        return self.path / "LocalStorage"

    @property
    def app_settings_file_path(self):
        return self.local_storage_folder_path / "appStorage.json"

    def get_cached_fflags(self) -> Dict[str, Any]:
        with open(
                file=self.studio_app_settings_file_path,
                mode="rb"
        ) as file:
            data = file.read()
        return orjson.loads(data)

    def get_app_storage(self):
        with open(
                file=self.app_settings_file_path,
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

    def get_cookies(self) -> Dict[str, Dict[str, RobloxCookie]]:
        """
        Gets the stored cookies for the current Roblox session.

        Returns:
            A dictionary where the keys are cookie hosts (e.g. "roblox.com") and the values are dictionaries where the
            keys are the names of the cookie (e.g. ".ROBLOSECURITY") and the values are the RobloxCookie objects themselves.

            Example: {"roblox.com": {".ROBLOSECURITY": RobloxCookie}}
        """
        cookie_dict = {}
        raw_cookie_dict = get_raw_settings("RobloxStudioBrowser")

        for url, raw_cookies in raw_cookie_dict.items():
            new_cookies = {}
            for cookie_name, raw_cookie_value in raw_cookies.items():
                new_cookies[cookie_name] = RobloxCookie.from_raw_string(raw_cookie_value)
            cookie_dict[url] = new_cookies

        return cookie_dict

    def set_cookies(self, cookies: Dict[str, Dict[str, RobloxCookie]]):
        raw_cookie_dict = {}

        for url, url_cookies in cookies.items():
            raw_cookie_dict[url] = {cookie_name: cookie.to_raw_string() for cookie_name, cookie in url_cookies.items()}

        return raw_cookie_dict
