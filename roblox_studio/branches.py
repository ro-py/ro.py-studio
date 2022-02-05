from yarl import URL
from enum import Enum


class RobloxBranch(Enum):
    production = "production"

    sitetest1 = "sitetest1"
    sitetest2 = "sitetest2"
    sitetest3 = "sitetest3"

    gametest1 = "gametest1"
    gametest2 = "gametest2"


roblox_branch_to_url = {
    RobloxBranch.production: URL("https://setup.rbxcdn.com/"),

    RobloxBranch.sitetest1: URL("http://setup.sitetest1.robloxlabs.com.s3.amazonaws.com/"),
    RobloxBranch.sitetest2: URL("http://setup.sitetest2.robloxlabs.com.s3.amazonaws.com/"),
    RobloxBranch.sitetest3: URL("http://setup.sitetest3.robloxlabs.com.s3.amazonaws.com/"),

    RobloxBranch.gametest1: URL("http://setup.gametest1.robloxlabs.com.s3.amazonaws.com/"),
    RobloxBranch.gametest2: URL("http://setup.gametest2.robloxlabs.com.s3.amazonaws.com/")
}
