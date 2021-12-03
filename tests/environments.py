import asyncio
from roblox_studio import StudioClient


async def main():
    studio_client = StudioClient()
    environments = await studio_client.get_environments()
    for environment in environments:
        print(environment.name)
        print(f"\tVersion: {environment.version}")
        print(f"\tBootstrapper Path: {environment.bootstrapper_path}")
        print(f"\tPath: {environment.get_version_path()}")


if __name__ == "__main__":
    asyncio.run(main())
