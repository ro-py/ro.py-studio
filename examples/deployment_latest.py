import asyncio

from roblox_studio.branches import RobloxBranch
from roblox_studio.deployments import DeploymentClient, DeploymentType, OperatingSystem


async def main():
    async with DeploymentClient() as deployment_client:
        deployments = await deployment_client.get_deployments(
            branch=RobloxBranch.production,
            operating_system=OperatingSystem.windows
        )
        deployment = deployments.get_latest_deployment(DeploymentType.studio)
        print(f"Version Number: {deployment.version_number}")
        print(f"Version: {deployment.version_hash}")
        print(f"Type: {deployment.deployment_type}")
        print(f"Timestamp: {deployment.timestamp}")
        print(f"Git Hash: {deployment.git_hash}")


asyncio.get_event_loop().run_until_complete(main())
