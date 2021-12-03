import asyncio
from roblox_studio import StudioClient


async def main():
    studio_client = StudioClient()
    settings = await studio_client.get_settings()
    print(await settings.to_xml())


if __name__ == "__main__":
    asyncio.run(main())
