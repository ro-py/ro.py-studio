import asyncio
from typing import List, Optional
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from pathlib import Path

from .properties import Property, PropertyType, type_to_class


class SettingsItem:
    def __init__(self):
        self.type: Optional[str] = None
        self.referent: Optional[str] = None
        self.properties: List[Property] = []

    def from_tag(self, tag: Tag):
        # TODO: reconsider calling this "type" instead of class
        self.type = tag.get("class")
        self.referent = tag.get("referent")
        properties_tag = tag.find("Properties", recursive=False)
        self.properties = []
        for property_tag in properties_tag:
            if isinstance(property_tag, Tag):
                property_type = PropertyType(property_tag.name)
                property_class = type_to_class.get(property_type) or Property
                self.properties.append(property_class(property_tag))


def _settings_from_xml(markup: str):
    soup = BeautifulSoup(
        markup=markup,
        features="lxml-xml"
    )
    roblox_tag: Tag = soup.find("roblox")
    item_tags: ResultSet = roblox_tag.find_all("Item", recursive=False)
    version = int(roblox_tag.get("version"))
    items = []

    for item_tag in item_tags:
        settings_item = SettingsItem()
        settings_item.from_tag(item_tag)
        items.append(settings_item)

    return version, items


class Settings:
    """
    Represents a Roblox Studio XML settings file.
    """

    def __init__(self):
        self.version: Optional[int] = None
        self.items: List[SettingsItem] = []

    async def from_xml(self, markup: str):
        self.version, self.items = await asyncio.get_event_loop().run_in_executor(None, _settings_from_xml, markup)

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

    def _to_xml(self):
        return str(self.to_soup())

    async def to_xml(self):
        return await asyncio.get_event_loop().run_in_executor(None, self._to_xml)


class AppSettings:
    def __init__(self, version_path: Path):
        self._version_path: Path = version_path
        self.content_folder_name: Optional[str] = None
        self.base_url: Optional[str] = None

    def _from_xml(self, markup: str):
        soup = BeautifulSoup(
            markup=markup,
            features="lxml-xml"
        )
        settings_tag = soup.find("Settings")
        self.content_folder_name = settings_tag.find("ContentFolder").text
        self.base_url = settings_tag.find("BaseUrl").text

    async def from_xml(self, markup: str):
        await asyncio.get_event_loop().run_in_executor(None, self._from_xml, markup)

    def to_soup(self):
        soup = BeautifulSoup(features="lxml-xml")

        settings_tag: Tag = soup.new_tag("Settings")

        content_folder_tag: Tag = soup.new_tag("ContentFolder")
        content_folder_tag.string = self.content_folder_name

        base_url_tag: Tag = soup.new_tag("BaseUrl")
        base_url_tag.string = self.base_url

        settings_tag.append(content_folder_tag)
        settings_tag.append(base_url_tag)

        soup.append(settings_tag)
        return soup

    def _to_xml(self):
        return str(self.to_soup())

    async def to_xml(self):
        return await asyncio.get_event_loop().run_in_executor(None, self._to_xml)

    def get_content_folder(self):
        return self._version_path / self.content_folder_name
