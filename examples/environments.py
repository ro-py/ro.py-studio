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
        app_settings = await environment.get_app_settings()
        print("\tApp Settings:")
        print(f"\t\tBase URL: {app_settings.base_url}")
        print(f"\t\tContent Folder: {app_settings.get_content_folder()}")


if __name__ == "__main__":
    asyncio.run(main())
