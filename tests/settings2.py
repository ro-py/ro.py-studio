import asyncio
from roblox_studio import StudioClient


async def main():
    studio_client = StudioClient()
    settings = await studio_client.get_settings()
    physics_item = settings.get_item("PhysicsSettings")
    allow_sleep_property = physics_item.get_property("AllowSleep")
    print(f"Allow Physics Sleep={allow_sleep_property.value}")


if __name__ == "__main__":
    asyncio.run(main())
