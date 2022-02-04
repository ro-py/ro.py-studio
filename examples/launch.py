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
    process = studio_version.launch()
    print(f"🚀 Launched Roblox Studio with process ID {process.pid}")
    process.wait()
    print("Studio closed.")


if __name__ == "__main__":
    main()
