import asyncio

from roblox import Client

from roblox_studio.branches import RobloxBranch
from roblox_studio.deployments import DeploymentClient, DeploymentType

roblox = Client()
roblox_deploy = DeploymentClient(roblox)


async def main():
    deployments = await roblox_deploy.get_deployments(RobloxBranch.production)
    deployment = deployments.get_latest_version(DeploymentType.studio_64)
    print(f"Version: {deployment.version_hash}")
    print(f"Type: {deployment.deployment_type}")
    print(f"Timestamp: {deployment.timestamp}")
    print(f"Git Hash: {deployment.git_hash}")
    print(f"Bootstrapper Version: {deployment.bootstrapper_version}")


asyncio.get_event_loop().run_until_complete(main())
