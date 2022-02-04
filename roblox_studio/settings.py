from pathlib import Path
import os

if os.name == "nt":
    import winreg
elif os.name == "posix":
    import plistlib


def get_subkeys(key):
    index = 0

    while True:
        try:
            yield winreg.EnumKey(key, index)
        except OSError:
            break
        index += 1


def get_key_values(key):
    index = 0

    while True:
        try:
            yield winreg.EnumValue(key, index)
        except OSError:
            break
        index += 1


def key_to_dictionary(key):
    result = {}

    for value_name, value_data, value_type in get_key_values(key):
        result[value_name] = value_data

    for subkey_name in get_subkeys(key):
        subkey = winreg.OpenKeyEx(key, subkey_name)
        result[subkey_name] = key_to_dictionary(subkey)

    return result


def deep_rbx_dict_to_list(data):
    """
    Deeply converts "rbx dicts" (ie, dicts with ordered numeric keys) into proper lists.
    May not maintain order.
    """

    bad_dict: dict = data

    for key, value in bad_dict.items():
        if not isinstance(value, dict):
            continue

        bad_dict[key] = deep_rbx_dict_to_list(value)

    bad_keys = set(bad_dict.keys())
    numeric_keys = set()
    start_point = 0 if 0 in bad_keys else 1

    for bad_key in bad_keys:
        if bad_key.isnumeric():
            numeric_keys.add(int(bad_key))
        else:
            if bad_key != "size":
                # if there is a key in the dict other than size that is not numeric, this is not a proper list
                return bad_dict

    if numeric_keys != set(range(start_point, start_point + len(numeric_keys))):
        # if the keys are not in proper order with no gaps, this is not a proper list
        return bad_dict

    list_size = 0
    for bad_key in bad_keys:
        if bad_key.isnumeric():
            index = int(bad_key)
            if index > list_size:
                list_size = index

    new_list = [None for _ in range(list_size)]

    for bad_key in bad_keys:
        if bad_key.isnumeric():
            new_list[int(bad_key) - start_point] = bad_dict[bad_key]

    return new_list


def plist_data_to_rbx_dict(plist_data: dict) -> dict:
    """
    Converts data from a Roblox macOS .plist file into a dictionary.
    """
    rbx_dict: dict = {}
    for raw_key, raw_value in plist_data.items():
        split_key = raw_key.split(".")

        key_piece = rbx_dict

        for i, key_bit in enumerate(split_key):
            key_bit = key_bit.replace("\u00b7", ".")
            if i == len(split_key) - 1:
                if isinstance(raw_value, bytes):
                    raw_value = str(raw_value)
                key_piece[key_bit] = raw_value
                continue

            if key_piece.get(key_bit):
                key_piece = key_piece[key_bit]
            else:
                new_piece = {}
                key_piece[key_bit] = new_piece
                key_piece = new_piece
    return rbx_dict


def get_raw_settings(name: str):
    if os.name == "nt":
        key = winreg.OpenKeyEx(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=rf"SOFTWARE\Roblox\{name}"
        )

        settings = key_to_dictionary(key)
        settings = deep_rbx_dict_to_list(settings)

        key.Close()
    elif os.name == "posix":
        plist_path = Path("~/Library/Preferences").expanduser() / f"com.roblox.{name}.plist"

        with open(
                file=plist_path,
                mode="rb"
        ) as roblox_plist_file:
            plist_data = plistlib.load(roblox_plist_file)
        settings = plist_data_to_rbx_dict(plist_data)
        settings = deep_rbx_dict_to_list(settings)
    else:
        raise NotImplementedError("Unknown OS")

    return settings


if __name__ == '__main__':
    print(get_raw_settings("RobloxStudio"))
