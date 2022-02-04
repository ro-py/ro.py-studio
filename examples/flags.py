from typing import Optional
from pathlib import Path
import os
import asyncio

from roblox_studio import StudioClient
from roblox_studio.environments import Version


def main():
    studio_client = StudioClient()

    version_path: Optional[Path] = None
    if os.name == "nt":
        version_path = studio_client.paths.versions / "version-HASH"
    elif os.name == "posix":
        version_path = Path("/Applications/RobloxStudio.app")

    studio_version = studio_client.get_version(version_path)
    fflag_overrides = studio_version.get_fflag_overrides()
    fflag_overrides["FFlagDebugDisplayFPS"] = True
    studio_version.set_fflag_overrides(fflag_overrides)


if __name__ == "__main__":
    main()
