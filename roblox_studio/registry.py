class RobloxRegistry:
    def __init__(self, root_key: str):
        self.root = root_key
        self.retention = self.root + r"\Retention"
        self.roblox_studio = self.root + r"\RobloxStudio"
        self.roblox_studio_browser = self.root + r"\RobloxStudioBrowser"
        self.splash_screen = self.root + r"\SplashScreen"


class RobloxCorpRegistry:
    def __init__(self, root_key: str):
        self.root = root_key
        self.environments = self.root + r"\Environments"
        self.roblox = self.root + r"\Roblox"
