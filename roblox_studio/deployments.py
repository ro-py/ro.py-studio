from __future__ import annotations

from datetime import datetime
from enum import Enum
from re import search
from typing import List, Optional, Union

from dateutil.parser import parse
from roblox import Client
from roblox.utilities.shared import ClientSharedObject

from .branches import RobloxBranch


class DeploymentType(Enum):
    rcc_service = "RccService"

    client = "Client"
    windows_player = "WindowsPlayer"

    studio = "Studio"
    studio_64 = "Studio64"
    studio_beta = "StudioBeta"
    mfc_studio = "MFCStudio"

    windows_mfc_player_and_studio = "windows-mfc-player-and-studio"


class DeploymentPackage:
    def __init__(self, shared: ClientSharedObject, branch: RobloxBranch, deployment: Deployment, lines: List[str]):
        self._branch: RobloxBranch = branch
        self._shared: ClientSharedObject = shared
        self._deployment: Deployment = deployment

        self.name: str = lines[0]
        self.md5: str = lines[1]
        self.compressed_size: int = int(lines[2])
        self.size: int = int(lines[3])


class DeploymentPackages:
    def __init__(self, shared: ClientSharedObject, branch: RobloxBranch, deployment: Deployment, packages_data: str):
        self._branch: RobloxBranch = branch
        self._shared: ClientSharedObject = shared
        self._deployment: Deployment = deployment

        self.packages: List[DeploymentPackage] = []

        packages_lines = packages_data.splitlines()
        packages_file_lines = packages_lines[1:]

        self.version: str = packages_lines[0]

        for i in range(0, len(packages_file_lines), 4):
            file_lines = packages_file_lines[i:i + 4]
            self.packages.append(DeploymentPackage(
                shared=self._shared,
                branch=self._branch,
                deployment=self._deployment,
                lines=file_lines
            ))


class Deployment:
    def __init__(self, shared: ClientSharedObject, branch: RobloxBranch, history_line: str):
        self._branch: RobloxBranch = branch
        self._shared: ClientSharedObject = shared

        self.deployment_type: DeploymentType
        self.version_hash: str
        self.timestamp: datetime
        self.bootstrapper_version: Optional[str] = None
        self.git_hash: Optional[str] = None

        if "git hash" in history_line:
            match = search(
                r"New ([^ ]*?) (version-[^ ]*) at ([^ ]*) (.*?), file version: ([0123456789, ]*), git hash: ("
                r"[^ ]*)",
                string=history_line
            )

            self.deployment_type = DeploymentType(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")
            self.bootstrapper_version = match.group(5)
            self.git_hash = match.group(6)
        elif "file version" in history_line or "file verion" in history_line:
            match = search(
                r"New ([^ ]*?) (version-[^ ]*) at ([^ ]*) (.*?), file vers?ion: ([0123456789, ]*)",
                string=history_line
            )

            self.deployment_type = DeploymentType(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")
            self.bootstrapper_version = match.group(5)
        else:
            match = search(
                r"New ([^ ]*?) (version-[^ ]*) at ([^ ]*) (.*)",
                string=history_line
            )

            self.deployment_type = DeploymentType(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")

    async def get_packages(self):
        packages_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                subdomain="s3",
                base_url="amazonaws.com",
                path=f"setup.{self._branch.value}.com/{self.version_hash}-rbxPkgManifest.txt"
            )
        )
        return DeploymentPackages(
            branch=self._branch,
            shared=self._shared,
            deployment=self,
            packages_data=packages_response.text
        )


class DeploymentRevert:
    def __init__(self, shared: ClientSharedObject, branch: RobloxBranch, history_line: str):
        self._branch: RobloxBranch = branch
        self._shared: ClientSharedObject = shared

        self.deployment_type: DeploymentType
        self.version_hash: str
        self.timestamp: datetime
        self.bootstrapper_version: Optional[str] = None
        self.git_hash: Optional[str] = None

        if history_line.startswith("Reverting"):
            match = search(r"Reverting ([^ ]*?) to version (version-[^ ]*) at ([^ ]*) (.*)", history_line)
            self.deployment_type = DeploymentType(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")
        else:
            match = search(r"Revert ([^ ]*?) (version-[^ ]*) at ([^ ]*) (.*)", history_line)
            self.deployment_type = DeploymentType(match.group(1))
            self.version_hash = match.group(2)
            date_string = match.group(3)
            time_string = match.group(4)
            self.timestamp = parse(f"{date_string} {time_string}")


class DeploymentHistory:
    def __init__(self, shared: ClientSharedObject, branch: RobloxBranch, history_data: str):
        self._shared: ClientSharedObject = shared
        self._branch: RobloxBranch = branch
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

                if history_subline.startswith("New"):
                    self.history.append(Deployment(
                        shared=self._shared,
                        branch=self._branch,
                        history_line=history_subline
                    ))
                elif history_subline.startswith("Revert"):
                    self.history.append(DeploymentRevert(
                        shared=self._shared,
                        branch=self._branch,
                        history_line=history_subline
                    ))

    def get_latest_version(self, deployment_type: DeploymentType) -> Optional[Deployment]:
        for deployment in reversed(self.history):
            if deployment.deployment_type == deployment_type:
                return deployment
        return None


class DeploymentClient:
    def __init__(self, client: Client):
        self._roblox: Client = client
        self._shared: ClientSharedObject = self._roblox._shared

    async def get_deployments(self, branch: RobloxBranch):
        history_response = await self._roblox.requests.get(
            url=self._roblox.url_generator.get_url(
                subdomain="s3",
                base_url="amazonaws.com",
                path=f"setup.{branch.value}.com/DeployHistory.txt"
            )
        )
        return DeploymentHistory(
            shared=self._shared,
            branch=branch,
            history_data=history_response.text
        )
