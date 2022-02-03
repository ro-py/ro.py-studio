import asyncio

from roblox_studio import StudioClient
from roblox_studio.environments import Version


async def main():
    studio_client = StudioClient()
    studio_version = studio_client.get_version(studio_client.paths.versions / "version-HASH")
    fflag_overrides = await studio_version.get_fflag_overrides()
    fflag_overrides["FFlagDebugDisplayFPS"] = True
    await studio_version.set_fflag_overrides(fflag_overrides)


if __name__ == "__main__":
    asyncio.run(main())
