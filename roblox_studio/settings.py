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

    def to_soup(self):
        soup = BeautifulSoup(features="lxml-xml")
        soup.is_xml = False  # hack to stop it from adding xml tags

        roblox_tag: Tag = soup.new_tag(
            name="roblox",
            attrs={
                "xmlns:xmime": "http://www.w3.org/2005/05/xmlmime",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:noNamespaceSchemaLocation": "http://www.roblox.com/roblox.xsd",
                "version": str(self.version)
            }
        )

        external_1 = soup.new_tag(name="External")
        external_1.string = "null"
        external_2 = soup.new_tag(name="External")
        external_2.string = "nil"

        roblox_tag.append(external_1)
        roblox_tag.append(external_2)

        soup.append(roblox_tag)

        for item in self.items:
            item_tag = soup.new_tag(
                name="Item",
                attrs={
                    "class": item.type,
                    "referent": item.referent
                }
            )
            properties_tag = soup.new_tag("Properties")

            for property in item.properties:
                property_tag = soup.new_tag(
                    name=property.type.value,
                    attrs={
                        "name": property.name
                    }
                )

                for element in property.to_elements(soup):
                    property_tag.append(element)

                properties_tag.append(property_tag)

            item_tag.append(properties_tag)
            roblox_tag.append(item_tag)

        return soup

    def to_xml(self):
        soup = self.to_soup()
        return str(soup)
