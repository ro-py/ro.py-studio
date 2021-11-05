from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet

from .properties import Property, PropertyType, type_to_class


class SettingsItem:
    def __init__(self, tag: Tag):
        # TODO: reconsider calling this "type" instead of class
        self.type: str = tag.get("class")
        self.referent: str = tag.get("referent")
        properties_tag = tag.find("Properties", recursive=False)
        self.properties: List[Property] = []
        for property_tag in properties_tag:
            if isinstance(property_tag, Tag):
                property_type = PropertyType(property_tag.name)
                property_class = type_to_class.get(property_type) or Property
                self.properties.append(property_class(property_tag))


class Settings:
    """
    Represents a Roblox Studio XML settings file.
    """
    def __init__(self, soup: BeautifulSoup):
        roblox_tag: Tag = soup.find("roblox")
        item_tags: ResultSet = roblox_tag.find_all("Item", recursive=False)

        self.version: int = int(roblox_tag.get("version"))
        self.items: List[SettingsItem] = [
            SettingsItem(item_tag) for item_tag in item_tags
        ]
