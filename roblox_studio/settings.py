from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet


class StudioSettingsItem:
    def __init__(self, tag: Tag):
        # TODO: reconsider calling this "type" instead of class
        self.type: str = tag.get("class")[0]
        self.referent: str = tag.get("referent")


class StudioSettings:
    """
    Represents a Roblox Studio XML settings file.
    """
    def __init__(self, soup: BeautifulSoup):
        roblox_tag: Tag = soup.find("roblox")
        item_tags: ResultSet = roblox_tag.find_all("item")

        self.items: List[StudioSettingsItem] = [
            StudioSettingsItem(item_tag) for item_tag in item_tags
        ]
