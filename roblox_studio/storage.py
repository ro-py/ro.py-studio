from enum import IntEnum, Enum
from typing import Optional, List

import orjson

from .utilities import int_or_none


class MembershipType(IntEnum):
    """
    Represents a Roblox membership type.
    Please see https://developer.roblox.com/en-us/api-reference/enum/MembershipType for more information.
    """
    none = 0
    builders_club = 1
    turbo_builders_club = 2
    outrageous_builders_club = 3
    premium = 4


class PolicyServiceHttpResponse:
    def __init__(self, data: dict):
        self.is_subject_to_china_policies: bool = data["isSubjectToChinaPolicies"]
        self.are_paid_random_items_restricted: bool = data["arePaidRandomItemsRestricted"]
        self.is_paid_item_trading_allowed: bool = data["isPaidItemTradingAllowed"]
        self.allowed_external_link_references: List[str] = data["allowedExternalLinkReferences"]


class Theme(Enum):
    dark = "dark"
    light = "light"


class AppStorage:
    def __init__(self, data: dict):
        self.app_installation_id: Optional[int] = int_or_none(data.get("AppInstallationId"))
        self.username: Optional[str] = data.get("Username")
        self.membership: Optional[MembershipType] = MembershipType(int(data["Membership"])) if data.get("Membership") \
            else None
        self.roblox_locale_id: Optional[str] = data.get("RobloxLocaleId")
        self.browser_tracker_id: Optional[int] = int_or_none(data.get("BrowserTrackerId"))

        self.web_login: Optional[int] = int_or_none(data.get("WebLogin"))
        # rethink where to do these orjson loads. this is probably bad
        self.policy_service_http_response: Optional[PolicyServiceHttpResponse] = \
            PolicyServiceHttpResponse(orjson.loads(data["PolicyServiceHttpResponse"])) \
            if data.get("PolicyServiceHttpResponse") else None

        self.player_exe_launch_time: Optional[int] = int_or_none(data.get("PlayerExeLaunchTime"))
        self.user_id: Optional[int] = int_or_none(data.get("UserId"))
        self.is_under_13: Optional[int] = (True if data["IsUnder13"] == "true" else "false") if data.get("IsUnder13") \
            else None
        self.display_name: Optional[str] = data.get("DisplayName")
        self.country_code: Optional[str] = data.get("CountryCode")
        self.game_locale_id: Optional[str] = data.get("GameLocaleId")
        self.authenticated_theme: Optional[Theme] = Theme(data["AuthenticatedTheme"]) \
            if data.get("AuthenticatedTheme") else None
        self.experience_menu_version: Optional[str] = data.get("ExperienceMenuVersion")
        self.native_close_lua_prompt_display_count: Optional[dict] = \
            orjson.loads(data["NativeCloseLuaPromptDisplayCount"]) if data.get("NativeCloseLuaPromptDisplayCount") \
            else None
