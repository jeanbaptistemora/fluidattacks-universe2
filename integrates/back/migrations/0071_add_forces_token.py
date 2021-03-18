"""
This migration copies the existing integrates tokens from an old (makeshift)
forces infra to the new infra dedicated only for integrates

Execution Time:    Fri Feb 12 12:16:45 -05 2021
Finalization Time: Fri Feb 12 12:18:20 -05 2021
"""
# Standar library
import os
from typing import Optional

# Third library
import boto3
from botocore.exceptions import ClientError
import aioextensions

# Local library
from backend.domain import project as project_domain
from forces.domain import update_token


async def get_old_forces_token(group: str) -> Optional[str]:
    client = boto3.client(
        'secretsmanager',
        aws_access_key_id='serves_prod_key',
        aws_secret_access_key='serves_prod_secret',
    )  # nosec
    try:
        response = await aioextensions.in_thread(
            client.get_secret_value,
            SecretId=f'forces-token-{group}',
        )
    except ClientError as exc:
        print(f'[ERROR] {group}', exc)
        return None
    return response.get('SecretString')  # type: ignore


@aioextensions.run_decorator  # type: ignore
async def main() -> None:
    projects = await project_domain.get_projects_with_forces()
    for project in projects:
        print(f'[INFO] processing {project}')
        current_token = await get_old_forces_token(project)
        if current_token:
            if await update_token(project, current_token):
                print(f'[OK] {project}')
            else:
                print(f'[FAIL] {project}')


if __name__ == '__main__':
    main()
