from __future__ import annotations

from typing import List, Optional, Literal, Union, Any, Set
from pydantic import BaseModel, conlist
from enum import Enum
import logging


class FilterType(str, Enum):
    place_filter = "place_filter"
    data_center_filter = "data_center_filter"


class FlagKind(str, Enum):
    static = "static"
    synced = "synced"
    dynamic = "dynamic"


_flag_prefix_to_kind = {
    "F": FlagKind.static,
    "SF": FlagKind.synced,
    "DF": FlagKind.dynamic
}
_flag_kind_to_prefix = {v: k for k, v in _flag_prefix_to_kind.items()}

_flag_suffix_to_type = {
    "PlaceFilter": FilterType.place_filter,
    "DataCenterFilter": FilterType.data_center_filter
}
_flag_type_to_suffix = {v: k for k, v in _flag_suffix_to_type.items()}


class FlagType(str, Enum):
    flag = "flag"
    int = "int"
    string = "string"
    log = "log"


_flag_type_to_class = {}
_flag_type_to_filter_class = {}


class FlagFilter(BaseModel):
    type: FilterType
    values: List[int]


class GenericFlag(BaseModel):
    kind: Optional[FlagKind]  # only optional because of stupid
    type: Optional[FlagType]
    name: str
    filter: Optional[None]
    value: Any

    def get_raw_name(self):
        prefix = f"{_flag_kind_to_prefix[self.kind] if self.kind else ''}{self.type.value.title() if self.type else ''}"
        suffix = f"_{_flag_type_to_suffix[self.filter.type]}" if self.filter else ""

        return f"{prefix}{self.name}{suffix}"

    def get_raw_value(self):
        if self.filter:
            return ";".join([str(self.value)] + [str(value) for value in self.filter.values])
        else:
            return self.value

    @classmethod
    def from_raw(cls, name: str, value: Any):
        flag_kind = None
        flag_type = None
        flag_filter_type = None
        flag_filter = None

        string_index = 0

        for prefix, kind in _flag_prefix_to_kind.items():
            if name.startswith(prefix):
                flag_kind = kind
                string_index += len(prefix)
                break

        # assert flag_kind, "Flag has improper prefix."

        for type in FlagType:
            if name[string_index:].startswith(type.value.title()):
                flag_type = type
                string_index += len(flag_type.value)
                break

        # assert flag_type, "Invalid flag type name."

        root_name = name[string_index:]

        for suffix, filter_type in _flag_suffix_to_type.items():
            if root_name.endswith(f"_{suffix}"):
                flag_filter_type = filter_type
                root_name = root_name[:-len(suffix) - 1]
                break

        if flag_filter_type:
            split_value: List[str] = value.split(";")
            value = split_value[0]
            filter_values = [int(raw_value) for raw_value in split_value[1:]]

            flag_filter = FlagFilter(
                type=filter_type,
                values=filter_values
            )

            flag_class = _flag_type_to_filter_class.get(flag_type) if flag_type else GenericFilterFlag
            print(root_name, flag_class)
        else:
            flag_class = _flag_type_to_class.get(flag_type) if flag_type else GenericFlag

        return flag_class(
            kind=flag_kind,
            type=flag_type,
            name=root_name,
            value=value,
            filter=flag_filter
        )


class GenericFilterFlag(GenericFlag):
    filter: FlagFilter


class Flag(GenericFlag):
    type: Literal[FlagType.flag] = FlagType.flag
    value: bool


class IntFlag(GenericFlag):
    type: Literal[FlagType.int] = FlagType.int
    value: int


class StringFlag(GenericFlag):
    type: Literal[FlagType.string] = FlagType.string
    value: str


class LogFlag(GenericFlag):
    type: Literal[FlagType.log] = FlagType.log
    value: int


class FilterFlag(GenericFilterFlag):
    type: Literal[FlagType.flag] = FlagType.flag
    value: bool


class FilterIntFlag(GenericFilterFlag):
    type: Literal[FlagType.int] = FlagType.int
    value: int


class FilterStringFlag(GenericFilterFlag):
    type: Literal[FlagType.string] = FlagType.string
    value: str


class FilterLogFlag(GenericFilterFlag):
    type: Literal[FlagType.log] = FlagType.log
    value: int


class FlagContainer(BaseModel):
    flags: List[Union[
        FilterFlag, Flag,
        FilterIntFlag, IntFlag,
        FilterStringFlag, StringFlag,
        FilterLogFlag, LogFlag,
        GenericFilterFlag, GenericFlag
    ]]

    @classmethod
    def from_raw_dict(cls, data: dict) -> FlagContainer:
        flags = list()
        for raw_flag_name, raw_flag_value in data.items():
            try:
                flags.append(GenericFlag.from_raw(raw_flag_name, raw_flag_value))
            except AssertionError:
                continue

        return cls(flags=flags)

    def to_raw_dict(self) -> dict:
        data = {}

        for flag in self.flags:
            flag_raw_name, flag_raw_value = flag.get_raw_name(), flag.get_raw_value()

            if data.get(flag_raw_name):
                logging.warning("Found duplicate flag key while converting to raw dict.")

            data[flag_raw_name] = flag_raw_value

        return data


_flag_type_to_class[FlagType.flag] = Flag
_flag_type_to_class[FlagType.int] = IntFlag
_flag_type_to_class[FlagType.string] = StringFlag
_flag_type_to_class[FlagType.log] = LogFlag

_flag_type_to_filter_class[FlagType.flag] = FilterFlag
_flag_type_to_filter_class[FlagType.int] = FilterIntFlag
_flag_type_to_filter_class[FlagType.string] = FilterStringFlag
_flag_type_to_filter_class[FlagType.log] = FilterLogFlag
