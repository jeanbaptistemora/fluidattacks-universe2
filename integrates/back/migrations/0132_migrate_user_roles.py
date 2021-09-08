# pylint: disable=invalid-name
"""
This migration will map some old user roles to the following:
 - (Old)         -> (New)
 - Analyst       -> Hacker
 - Closer        -> Reattacker
 - Group Manager -> System Owner

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
import authz
from custom_types import (
    User as UserType,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import time
from typing import (
    cast,
    Dict,
    List,
)

# Constants
PROD: bool = False

TABLE_NAME: str = "fi_authz"


async def get_all_users(
    filtering_exp: object = "",
    data_attr: str = "",
) -> List[UserType]:
    scan_attrs = {}
    if filtering_exp:
        scan_attrs["FilterExpression"] = filtering_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(TABLE_NAME, scan_attrs)
    return cast(List[UserType], items)


async def process_user(user: Dict[str, str], new_role: str) -> bool:
    success = False
    if PROD:
        success = await authz.grant_group_level_role(
            user["subject"], user["object"], new_role
        )
    return success


async def migrate_roles(
    users: List[UserType], old_role: str, new_role: str
) -> None:
    success = all(
        await collect(process_user(user, new_role) for user in users)
    )
    print(f"{old_role}s migrated: {success}")


async def main() -> None:
    authz_users = await get_all_users()

    analyst_users = [
        user for user in authz_users if user.get("role", "") == "analyst"
    ]
    closer_users = [
        user for user in authz_users if user.get("role", "") == "closer"
    ]
    gm_users = [
        user for user in authz_users if user.get("role", "") == "group_manager"
    ]

    migrate_roles(analyst_users, "analyst", "hacker")
    migrate_roles(closer_users, "closer", "reattacker")
    migrate_roles(gm_users, "group_manager", "system_owner")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
