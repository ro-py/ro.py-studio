from enum import Enum
from typing import List, Optional, Literal, Union
from pydantic import BaseModel, Field


class ThreadSafety(Enum):
    read_safe = "ReadSafe"
    unsafe = "Unsafe"
    safe = "Safe"


class SecurityLevel(Enum):
    none = "None"
    roblox_place_security = "RobloxPlaceSecurity"
    plugin_security = "PluginSecurity"
    local_user_security = "LocalUserSecurity"
    roblox_script_security = "RobloxScriptSecurity"
    roblox_security = "RobloxSecurity"
    not_accessible_security = "NotAccessibleSecurity"


class ClassTag(Enum):
    not_creatable = "NotCreatable"
    not_browsable = "NotBrowsable"
    service = "Service"
    not_replicated = "NotReplicated"
    deprecated = "Deprecated"
    player_replicated = "PlayerReplicated"
    settings = "Settings"
    user_settings = "UserSettings"


class MemoryCategory(Enum):
    instances = "Instances"
    animation = "Animation"
    physics_parts = "PhysicsParts"
    graphics_texture = "GraphicsTexture"
    gui = "Gui"
    script = "Script"
    internal = "Internal"


class MemberSerialization(BaseModel):
    can_load: bool = Field(alias="CanLoad")
    can_save: bool = Field(alias="CanSave")


class MemberSecurity(BaseModel):
    read: SecurityLevel = Field(alias="Read")
    write: SecurityLevel = Field(alias="Write")


class ValueType(BaseModel):
    category: str = Field(alias="Category")
    name: str = Field(alias="Name")


class ClassMemberProperty(BaseModel):
    member_type: Literal["Property"] = Field(alias="MemberType")
    name: str = Field(alias="Name")
    category: str = Field(alias="Category")
    security: MemberSecurity = Field(alias="Security")
    serialization: MemberSerialization = Field(alias="Serialization")
    thread_safety: ThreadSafety = Field(alias="ThreadSafety")
    value_type: ValueType = Field(alias="ValueType")


class FunctionParameter(BaseModel):
    name: str = Field(alias="Name")
    type: ValueType = Field(alias="Type")


class ClassMemberFunction(BaseModel):
    member_type: Literal["Function"] = Field(alias="MemberType")
    name: str = Field(alias="Name")
    parameters: List[FunctionParameter] = Field(alias="Parameters")
    return_type: ValueType = Field(alias="ReturnType")
    security: SecurityLevel = Field(alias="Security")
    thread_safety: ThreadSafety = Field(alias="ThreadSafety")


class ClassMemberEvent(BaseModel):
    member_type: Literal["Event"] = Field(alias="MemberType")
    name: str = Field(alias="Name")
    parameters: List[FunctionParameter] = Field(alias="Parameters")
    security: SecurityLevel = Field(alias="Security")
    thread_safety: ThreadSafety = Field(alias="ThreadSafety")


class ClassMemberCallback(BaseModel):
    member_type: Literal["Callback"] = Field(alias="MemberType")
    name: str = Field(alias="Name")
    parameters: List[FunctionParameter] = Field(alias="Parameters")
    return_type: ValueType = Field(alias="ReturnType")
    security: SecurityLevel = Field(alias="Security")
    thread_safety: ThreadSafety = Field(alias="ThreadSafety")


class APIDumpClass(BaseModel):
    members: List[Union[ClassMemberProperty, ClassMemberFunction, ClassMemberEvent, ClassMemberCallback]] = Field(alias="Members")
    tags: Optional[List[ClassTag]] = Field(None, alias="Tags")
    superclass: str = Field(alias="Superclass")
    name: str = Field(alias="Name")
    memory_category: MemoryCategory = Field(alias="MemoryCategory")


class APIDumpEnumItem(BaseModel):
    name: str = Field(alias="Name")
    value: int = Field(alias="Value")


class APIDumpEnum(BaseModel):
    items: List[APIDumpEnumItem] = Field(alias="Items")
    name: str = Field(alias="Name")


class APIDump(BaseModel):
    classes: List[APIDumpClass] = Field(alias="Classes")
    enums: List[APIDumpEnum] = Field(alias="Enums")
    version: int = Field(alias="Version")
