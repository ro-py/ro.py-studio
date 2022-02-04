import os

if os.name == "nt":
    import winreg
elif os.name == "posix":
    import plistlib


def get_subkeys(key: winreg.HKEYType):
    index = 0

    while True:
        try:
            yield winreg.EnumKey(key, index)
        except OSError:
            break
        index += 1


def get_key_values(key: winreg.HKEYType):
    index = 0

    while True:
        try:
            yield winreg.EnumValue(key, index)
        except OSError:
            break
        index += 1


def key_to_dictionary(key: winreg.HKEYType):
    result = {}

    for subkey_name in get_subkeys(key):
        subkey = winreg.OpenKeyEx(key, subkey_name)
        result[subkey_name] = key_to_dictionary(subkey)

        print(f"\t{subkey_name}")
        for value_name, value_data, value_type in get_key_values(subkey):
            result[subkey_name][value_name] = value_data
            print(f"\t\t{value_name} = {value_data}")

    return result


def get_raw_settings():
    settings = {}

    if os.name == "nt":
        key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Roblox\RobloxStudio")

        settings = key_to_dictionary(key)

        key.Close()
    else:
        raise NotImplementedError

    return settings


if __name__ == '__main__':
    print(get_raw_settings())
