import asyncio
from roblox_studio import StudioClient


async def main():
    studio_client = StudioClient()
    studio_environment = await studio_client.get_studio_environment()
    await studio_environment.set_fflag_overrides({
        "FFlagDebugDisplayFPS": True
    })

if __name__ == "__main__":
    asyncio.run(main())
