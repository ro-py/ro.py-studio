import asyncio

from roblox import Client

from roblox_studio.branches import RobloxBranch
from roblox_studio.deployments import DeploymentClient

roblox = Client()
roblox_deploy = DeploymentClient(roblox)


async def main():
    deployments = await roblox_deploy.get_deployments(RobloxBranch.production)
    for deployment in deployments.history:
        print(deployment.version_hash)
        print(f"\tType: {deployment.deployment_type}")
        print(f"\tTimestamp: {deployment.timestamp}")
        print(f"\tGit Hash: {deployment.git_hash}")
        print(f"\tBootstrapper Version: {deployment.bootstrapper_version}")


asyncio.get_event_loop().run_until_complete(main())
