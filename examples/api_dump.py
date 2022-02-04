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

    for dump_class in dump.classes:
        print(dump_class.name)
        print(f"\tSuperclass: {dump_class.superclass}")
        print(f"\tMemory Category: {dump_class.memory_category}")
        print(f"\tMembers: {len(dump_class.members)}")
        if dump_class.tags:
            print(f"\tTags: {dump_class.tags}")


if __name__ == "__main__":
    main()
