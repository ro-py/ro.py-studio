from roblox_studio import StudioClient


def main():
    studio_client = StudioClient()
    settings = studio_client.get_settings()
    for item in settings.items:
        for property in item.properties:
            # print(property.name, property.type)
            print(property)


if __name__ == "__main__":
    main()
