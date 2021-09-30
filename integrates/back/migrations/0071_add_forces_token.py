# pylint: disable=invalid-name
"""
This migration copies the existing integrates tokens from an old (makeshift)
forces infra to the new infra dedicated only for integrates

Execution Time:    Fri Feb 12 12:16:45 -05 2021
Finalization Time: Fri Feb 12 12:18:20 -05 2021
"""

import aioextensions
import boto3
from botocore.exceptions import (
    ClientError,
)
from forces.domain import (
    update_token,
)
from groups.domain import (
    get_groups_with_forces,
)
from typing import (
    Optional,
)


async def get_old_forces_token(group: str) -> Optional[str]:
    # pylint: disable=unsubscriptable-object
    client = boto3.client(  # nosec
        "secretsmanager",
        aws_access_key_id="serves_prod_key",
        aws_secret_access_key="serves_prod_secret",
    )  # nosec
    try:
        response = await aioextensions.in_thread(
            client.get_secret_value,
            SecretId=f"forces-token-{group}",
        )
    except ClientError as exc:
        print(f"[ERROR] {group}", exc)
        return None
    return response.get("SecretString")


@aioextensions.run_decorator
async def main() -> None:
    projects = await get_groups_with_forces()
    for project in projects:
        print(f"[INFO] processing {project}")
        current_token = await get_old_forces_token(project)
        if current_token:
            if await update_token(project, current_token):
                print(f"[OK] {project}")
            else:
                print(f"[FAIL] {project}")


if __name__ == "__main__":
    main()
