import asyncio
from roblox_studio import StudioClient


async def main():
    studio_client = StudioClient()
    settings = await studio_client.get_settings()
    for settings_item in settings.items:
        print(settings_item.type)
        for settings_property in settings_item.properties:
            print(f"\t{settings_property.name}={settings_property.value}")

if __name__ == "__main__":
    asyncio.run(main())
