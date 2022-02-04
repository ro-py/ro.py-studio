import datetime
from pydantic import BaseModel


def raw_cookie_to_dict(string: str) -> dict:
    result = {}
    string_pairs = string.split(",")
    for string_pair in string_pairs:
        raw_key, enclosed_raw_value = string_pair.strip().split("::")
        raw_value = enclosed_raw_value[1:-1]
        result[raw_key] = raw_value

    return result


def dict_to_raw_cookie(cookie_dict: dict) -> str:
    return ",".join(f"{raw_key}::<{raw_value}>" for raw_key, raw_value in cookie_dict.items())


class RobloxCookie(BaseModel):
    secure: bool
    expires: datetime.datetime
    value: str

    @classmethod
    def from_raw_string(cls, string: str):
        decoded_pairs = raw_cookie_to_dict(string)

        return cls(
            secure=True if decoded_pairs.get("SEC") and decoded_pairs["SEC"].lower() == "yes" else False,
            expires=decoded_pairs["EXP"],
            value=decoded_pairs["COOK"]
        )

    def to_raw_string(self):
        return dict_to_raw_cookie({
            "SEC": "YES" if self.secure else "NO",
            "EXP": self.expires.isoformat(),
            "COOK": self.value
        })


if __name__ == '__main__':
    cookie_string = "SEC::<YES>,EXP::<2052-01-27T20:58:25Z>,COOK::<TEST>"
    cookie = RobloxCookie.from_raw_string(cookie_string)
    print(cookie)
