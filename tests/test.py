from roblox_studio import StudioClient
from roblox_studio.properties import PropertyType


def main():
    studio_client = StudioClient()
    settings = studio_client.get_settings()
    for item in settings.items:
        print(item.type)
        for property in item.properties:
            print(f"\t{property.name} {property.type}")


if __name__ == "__main__":
    main()
