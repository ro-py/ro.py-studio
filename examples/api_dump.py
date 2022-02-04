from typing import Optional
from pathlib import Path
import os

from roblox_studio import StudioClient


def main():
    studio_client = StudioClient()

    version_path: Optional[Path] = None
    if os.name == "nt":
        version_path = Path(os.getenv("LocalAppData")) / "Roblox" / "Versions" / "version-HASH"
    elif os.name == "posix":
        version_path = Path("/Applications/RobloxStudio.app")

    studio_version = studio_client.get_version(version_path)
    dump = studio_version.generate_api_dump()
    print(dump)


if __name__ == "__main__":
    main()
