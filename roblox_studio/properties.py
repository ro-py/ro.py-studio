from enum import Enum
from bs4.element import Tag
from pathlib import Path


class PropertyType(Enum):
    bool = "bool"

    binary_string = "binarystring"
    string = "string"
    token = "token"

    float = "float"
    double = "double"
    int = "int"
    int64 = "int64"

    vector2 = "vector2"
    vector3 = "vector3"
    color3 = "color3"

    qdir = "qdir"
    qfont = "qfont"


class Property:
    def __init__(self, tag: Tag):
        self.name: str = tag.get("name")
        self.type: PropertyType = PropertyType(tag.name)
        self.raw_value: str = tag.text
        self.value = None

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r} type={self.type.name} value={self.value}>"


class PropertyQDir(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: Path = Path(self.raw_value.strip())


class Color3:
    def __init__(self, r: float, g: float, b: float):
        self.r: float = r
        self.g: float = g
        self.b: float = b

    def __repr__(self):
        return f"<{self.__class__.__name__} r={self.r} g={self.g} b={self.b}>"


class PropertyColor3(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: Color3 = Color3(
            r=float(tag.find("r").text),
            g=float(tag.find("g").text),
            b=float(tag.find("b").text)
        )

type_to_class = {
    PropertyType.qdir: PropertyQDir,
    PropertyType.color3: PropertyColor3
}
