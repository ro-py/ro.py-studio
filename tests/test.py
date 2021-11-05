from roblox_studio import StudioClient


def main():
    studio_client = StudioClient()
    settings = studio_client.get_settings()
    for item in settings.items:
        print(item.referent)
        print(item.type)


if __name__ == "__main__":
    main()
