from pathlib import Path


class StudioPaths:
    def __init__(self, root_path: Path):
        self.root: Path = root_path

        # Files
        self.global_settings: Path = self.root / "GlobalSettings_13.xml"
        self.global_basic_settings: Path = self.root / "GlobalBasicSettings_13.xml"
        self.analystics_settings: Path = self.root / "AnalysticsSettings.xml"  # what is this?

        # Folders
        self.logs: Path = self.root / "logs"
        self.local_storage: Path = self.root / "LocalStorage"
        self.installed_plugins: Path = self.root / "InstalledPlugins"
        self.client_settings: Path = self.root / "ClientSettings"

        # Subfiles
        self.app_storage: Path = self.local_storage / "appStorage.json"
        self.studio_app_settings: Path = self.client_settings / "StudioAppSettings.json"
