import asyncio
from roblox_studio import StudioClient


async def main():
    studio_client = StudioClient()
    studio_environment = await studio_client.get_studio_environment()
    fflag_overrides = await studio_environment.get_fflag_overrides()
    fflag_overrides["FFlagDebugDisplayFPS"] = True
    await studio_environment.set_fflag_overrides(fflag_overrides)

if __name__ == "__main__":
    asyncio.run(main())
