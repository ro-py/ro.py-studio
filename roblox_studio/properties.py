from enum import Enum
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag


class PropertyType(Enum):
    bool = "bool"

    binary_string = "BinaryString"
    string = "string"
    token = "token"

    float = "float"
    double = "double"
    int = "int"
    int64 = "int64"

    vector2 = "Vector2"
    vector3 = "Vector3"
    color3 = "Color3"

    qdir = "QDir"
    qfont = "QFont"


def decimal_if_needed(number: float):
    if number.is_integer():
        return str(int(number))
    else:
        return str(number)


# types:
class Color3:
    def __init__(self, r: float, g: float, b: float):
        self.r: float = r
        self.g: float = g
        self.b: float = b

    def __repr__(self):
        return f"<{self.__class__.__name__} r={self.r} g={self.g} b={self.b}>"


class Vector2:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __repr__(self):
        return f"<{self.__class__.__name__} x={self.x} y={self.y}>"


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __repr__(self):
        return f"<{self.__class__.__name__} x={self.x} y={self.y} z={self.z}>"


# properties:
class Property:
    def __init__(self, tag: Tag):
        self.name: str = tag.get("name")
        self.type: PropertyType = PropertyType(tag.name)
        self.raw_value: str = tag.text
        self.value = None

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r} type={self.type.name} value={self.value}>"

    def to_elements(self, soup: BeautifulSoup) -> list:
        # fallback in case of issue
        return [self.raw_value]


class PropertyQDir(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: Path = Path(self.raw_value.strip())

    def to_elements(self, soup: BeautifulSoup) -> list:
        return [self.value.as_posix()]


class PropertyColor3(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: Color3 = Color3(
            r=float(tag.find("R").text),
            g=float(tag.find("G").text),
            b=float(tag.find("B").text)
        )

    def to_elements(self, soup: BeautifulSoup) -> list:
        r_element = soup.new_tag(name="R")
        g_element = soup.new_tag(name="G")
        b_element = soup.new_tag(name="B")

        r_element.string = decimal_if_needed(self.value.r)
        g_element.string = decimal_if_needed(self.value.g)
        b_element.string = decimal_if_needed(self.value.b)

        return [r_element, g_element, b_element]


class PropertyInt(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: int = int(self.raw_value)

    def to_elements(self, soup: BeautifulSoup) -> list:
        return [str(self.value)]


class PropertyBool(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: bool = self.raw_value == "true"

    def to_elements(self, soup: BeautifulSoup) -> list:
        return ["true" if self.value is True else "false"]


class PropertyString(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: str = self.raw_value

    def to_elements(self, soup: BeautifulSoup) -> list:
        return [self.value]


class PropertyToken(Property):
    """
    Represents a token property, which is an integer representation of an Enum.
    """

    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: int = int(self.raw_value)

    def to_elements(self, soup: BeautifulSoup) -> list:
        return [str(self.value)]


class PropertyFloat(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: float = float(self.raw_value)

    def to_elements(self, soup: BeautifulSoup) -> list:
        return [decimal_if_needed(self.value)]


class PropertyVector2(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: Vector2 = Vector2(
            x=float(tag.find("X").text),
            y=float(tag.find("Y").text)
        )

    def to_elements(self, soup: BeautifulSoup) -> list:
        x_element = soup.new_tag(name="X")
        y_element = soup.new_tag(name="Y")

        x_element.string = decimal_if_needed(self.value.x)
        y_element.string = decimal_if_needed(self.value.y)

        return [x_element, y_element]


class PropertyVector3(Property):
    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.value: Vector3 = Vector3(
            x=float(tag.find("X").text),
            y=float(tag.find("Y").text),
            z=float(tag.find("Z").text)
        )

    def to_elements(self, soup: BeautifulSoup) -> list:
        x_element = soup.new_tag(name="X")
        y_element = soup.new_tag(name="Y")
        z_element = soup.new_tag(name="Z")

        x_element.string = decimal_if_needed(self.value.x)
        y_element.string = decimal_if_needed(self.value.y)
        z_element.string = decimal_if_needed(self.value.z)

        return [x_element, y_element, z_element]


type_to_class = {
    PropertyType.bool: PropertyBool,

    PropertyType.binary_string: PropertyString,
    PropertyType.string: PropertyString,
    PropertyType.token: PropertyToken,

    PropertyType.float: PropertyFloat,
    PropertyType.double: PropertyFloat,
    PropertyType.int: PropertyInt,
    PropertyType.int64: PropertyInt,

    PropertyType.color3: PropertyColor3,

    PropertyType.vector2: PropertyVector2,
    PropertyType.vector3: PropertyVector3,
    PropertyType.qdir: PropertyQDir
}
