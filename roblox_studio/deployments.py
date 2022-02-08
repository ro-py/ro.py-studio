from __future__ import annotations

# import warnings

from datetime import datetime
from enum import Enum
from re import compile
from typing import List, Optional, Union, Tuple

from yarl import URL
from aiohttp import ClientSession
from dateutil.parser import parse

from .branches import RobloxBranch, roblox_branch_to_url
from .dump import APIDump

cdn_url = URL("https://setup.rbxcdn.com/")
mac_cdn_url = cdn_url / "mac"

git_hash_pattern = compile(r"New ([^ ]*?) (version-[^ ]*) at ([^ ]*) (.*?), file version: ([0123456789, ]*), "
                           r"git hash: ?([^ ]*)")
file_version_pattern = compile(r"New ([^ ]*?) (version-[^ ]*) at ([^ ]*) (.*?), file vers?ion: ?([0123456789, ]*)")
fallback_pattern = compile(r"New ([^ ]*?) (version-[^ ]*) at ([^ ]*) (.*)")

reverting_pattern = compile(r"Reverting ([^ ]*?) to version (version-[^ ]*) at ([^ ]*) (.*)")
revert_pattern = compile(r"Revert ([^ ]*?) (version-[^ ]*) at ([^ ]*) (.*)")


class OperatingSystem(Enum):
    windows = "windows"
    mac = "mac"


class BinaryType(Enum):
    windows_player = "WindowsPlayer"
    windows_studio = "WindowsStudio"
    mac_player = "MacPlayer"
    mac_studio = "MacStudio"


class DeploymentType(Enum):
    rcc_service = "rcc_service"

    client = "client"
    windows_player = "windows_player"

    studio = "studio"
    studio_64 = "studio_64"
    studio_beta = "studio_beta"
    mfc_studio = "mfc_studio"

    windows_mfc_player_and_studio = "windows_mfc_player_and_studio"


_log_name_to_deployment_type = {
    "RccService": DeploymentType.rcc_service,
    "Client": DeploymentType.client,
    "WindowsPlayer": DeploymentType.windows_player,

    "Studio": DeploymentType.studio,
    "Studio64": DeploymentType.studio_64,
    "StudioBeta": DeploymentType.studio_beta,
    "MFCStudio": DeploymentType.mfc_studio,

    "windows-mfc-player-and-studio": DeploymentType.windows_mfc_player_and_studio
}


class DeploymentPackage:
    def __init__(self, client: DeploymentClient, branch: RobloxBranch, deployment: Deployment, lines: List[str]):
        self._branch: RobloxBranch = branch
        self._client: DeploymentClient = client
        self._deployment: Deployment = deployment

        self.name: str = lines[0]
        self.md5: str = lines[1]
        self.compressed_size: int = int(lines[2])
        self.size: int = int(lines[3])

    @property
    def url(self):
        return cdn_url / f"{self._deployment.version_hash}-{self.name}"


class DeploymentPackages:
    def __init__(self, client: DeploymentClient, branch: RobloxBranch, deployment: Deployment, packages_data: str):
        self._branch: RobloxBranch = branch
        self._client: DeploymentClient = client
        self._deployment: Deployment = deployment

        self.packages: List[DeploymentPackage] = []

        packages_lines = packages_data.splitlines()
        packages_file_lines = packages_lines[1:]

        self.version: str = packages_lines[0]

        for i in range(0, len(packages_file_lines), 4):
            file_lines = packages_file_lines[i:i + 4]
            self.packages.append(DeploymentPackage(
                client=self._client,
                branch=self._branch,
                deployment=self._deployment,
                lines=file_lines
            ))


class Deployment:
    def __init__(
            self,
            client: DeploymentClient,
            branch: RobloxBranch,
            operating_system: OperatingSystem,
            history_line: str
    ):
        self._branch: RobloxBranch = branch
        self._client: DeploymentClient = client
        self._operating_system: OperatingSystem = operating_system

        self.deployment_type: DeploymentType
        self.version_hash: str
        self.timestamp: datetime
        self.version_number: Optional[Tuple[int, int, int, int]] = None
        self.git_hash: Optional[str] = None

        if "git hash" in history_line:
            match = git_hash_pattern.search(string=history_line)
            assert match

            self.deployment_type = _log_name_to_deployment_type.get(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")
            self.version_number = tuple(int(piece.strip()) for piece in match.group(5).split(","))
            self.git_hash = match.group(6)
        elif "file version" in history_line or "file verion" in history_line:
            match = file_version_pattern.search(string=history_line)
            assert match

            self.deployment_type = _log_name_to_deployment_type.get(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")
            self.version_number = tuple(int(piece.strip()) for piece in match.group(5).split(","))
        else:
            match = fallback_pattern.search(string=history_line)
            assert match

            self.deployment_type = _log_name_to_deployment_type.get(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")

    async def get_api_dump(self) -> APIDump:
        branch_url = roblox_branch_to_url.get(self._branch)
        branch_os_url = branch_url / "mac" if self._operating_system == OperatingSystem.mac else branch_url
        async with self._client.session.get(branch_os_url / f"{self.version_hash}-API-Dump.json") as dump_response:
            dump_response.raise_for_status()
            return APIDump(**await dump_response.json())

    async def get_packages(self) -> DeploymentPackages:
        assert self._operating_system == OperatingSystem.windows, "Cannot get packages for non-Windows installs"

        async with self._client.session.get(cdn_url / f"{self.version_hash}-rbxPkgManifest.txt") as packages_response:
            packages_response.raise_for_status()
            return DeploymentPackages(
                client=self._client,
                branch=self._branch,
                deployment=self,
                packages_data=await packages_response.text(encoding="utf-8")
            )


class DeploymentRevert:
    def __init__(
            self,
            client: DeploymentClient,
            branch: RobloxBranch,
            operating_system: OperatingSystem,
            history_line: str
    ):
        self._branch: RobloxBranch = branch
        self._client: DeploymentClient = client
        self._operating_system: OperatingSystem = operating_system

        self.deployment_type: DeploymentType
        self.version_hash: str
        self.timestamp: datetime
        self.bootstrapper_version: Optional[str] = None
        self.git_hash: Optional[str] = None

        if history_line.startswith("Reverting"):
            match = reverting_pattern.search(history_line)
            self.deployment_type = _log_name_to_deployment_type.get(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")
        else:
            match = revert_pattern.search(history_line)
            self.deployment_type = _log_name_to_deployment_type.get(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")


class DeploymentHistory:
    def __init__(
            self,
            client: DeploymentClient,
            branch: RobloxBranch,
            operating_system: OperatingSystem,
            history_data: str
    ):
        self._client: DeploymentClient = client
        self._branch: RobloxBranch = branch
        self._operating_system: OperatingSystem = operating_system

        self.history: List[Union[Deployment, DeploymentRevert]] = []

        history_split = history_data.splitlines()
        for history_line in history_split:
            history_line = history_line.strip()
            if not history_line:
                continue

            history_sublines = history_line.split("...")

            for history_subline in history_sublines:
                history_subline = history_subline.strip()

                if history_subline == "Done!" or history_subline == "Error!":
                    continue

                try:
                    if history_subline.startswith("New"):
                        self.history.append(Deployment(
                            client=self._client,
                            branch=self._branch,
                            operating_system=self._operating_system,
                            history_line=history_subline
                        ))
                    elif history_subline.startswith("Revert"):
                        self.history.append(DeploymentRevert(
                            client=self._client,
                            branch=self._branch,
                            operating_system=self._operating_system,
                            history_line=history_subline
                        ))
                except AssertionError:
                    pass
                    # warnings.warn(f"Failed to parse string {history_subline!r}")

    def get_latest_deployment(self, deployment_type: DeploymentType) -> Optional[Deployment]:
        for deployment in reversed(self.history):
            if deployment.deployment_type == deployment_type:
                return deployment
        return None


class DeploymentClient:
    def __init__(self):
        self.session = ClientSession(
            headers={
                "User-Agent": "Roblox/WinInet"
            }
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.session.close()

    async def get_deployments(self, branch: RobloxBranch, operating_system: OperatingSystem):
        branch_url = roblox_branch_to_url.get(branch)
        branch_os_url = branch_url / "mac" if operating_system == OperatingSystem.mac else branch_url

        async with self.session.get(branch_os_url / "DeployHistory.txt") as history_response:
            history_response.raise_for_status()
            return DeploymentHistory(
                client=self,
                branch=branch,
                operating_system=operating_system,
                history_data=await history_response.text(encoding="utf-8")
            )
