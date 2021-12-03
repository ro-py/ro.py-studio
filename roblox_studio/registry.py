class RobloxRegistryPaths:
    def __init__(self, root_key: str):
        self.root = root_key
        self.retention = self.root + "/Retention"
        self.roblox_studio = self.root + "/RobloxStudio"
        self.roblox_studio_browser = self.root + "/RobloxStudioBrowser"
        self.splash_screen = self.root + "/SplashScreen"


class RobloxCorpRegistryPaths:
    def __init__(self, root_key: str):
        self.root = root_key
        self.environments = self.root + "/Environments"
        self.roblox = self.root + "/Roblox"
