import winreg
from typing import Optional


def soft_query(key_path, name):
    try:
        value, value_type = winreg.QueryValueEx(key_path, name)
        return value, value_type
    except FileNotFoundError:
        return None, None


class Environment:
    def __init__(self, name: str = None):
        self.name: Optional[str] = name
        self.channel: Optional[str] = None

        self.current_player_url: Optional[str] = None
        self.current_player_version: Optional[str] = None

        self.current_qt_studio_url: Optional[str] = None
        self.current_qt_studio_version: Optional[str] = None

        self.protocol_handler_scheme: Optional[str] = None
        self.version: Optional[str] = None

    def load(self, key_path):
        self.channel, _ = soft_query(key_path, "channel")

        self.current_player_url, _ = soft_query(key_path, "curPlayerUrl")
        self.current_player_version, _ = soft_query(key_path, "curPlayerVer")

        self.current_qt_studio_url, _ = soft_query(key_path, "curQTStudioUrl")
        self.current_qt_studio_version, _ = soft_query(key_path, "curQTStudioVer")

        self.protocol_handler_scheme, _ = soft_query(key_path, "protocol handler scheme")
        self.version, _ = soft_query(key_path, "version")
