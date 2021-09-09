# pylint: disable=invalid-name
"""
This migration will map some old user roles to the following:
 - (Old)         -> (New)
 - Analyst       -> Hacker
 - Closer        -> Reattacker
 - Group Manager -> System Owner

Execution Time:    2021-09-09 at 14:01:08 UTC-05
Finalization Time: 2021-09-09 at 14:02:13 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from aiohttp.client_exceptions import (
    ClientError,
)
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
PROD: bool = True

AUTHZ_TABLE: str = "fi_authz"


async def get_all_users(
    filtering_exp: object = "",
    data_attr: str = "",
) -> List[UserType]:
    scan_attrs = {}
    if filtering_exp:
        scan_attrs["FilterExpression"] = filtering_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(AUTHZ_TABLE, scan_attrs)
    return cast(List[UserType], items)


async def update(
    subject: str, object_param: str, data: Dict[str, str]
) -> bool:
    """Manually updates db data"""
    success = False
    set_expression = ""
    remove_expression = ""
    expression_names = {}
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f"#{attr}, "
            expression_names.update({f"#{attr}": attr})
        else:
            set_expression += f"#{attr} = :{attr}, "
            expression_names.update({f"#{attr}": attr})
            expression_values.update({f":{attr}": value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        "Key": {
            "subject": subject,
            "object": object_param,
        },
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    if expression_names:
        update_attrs.update({"ExpressionAttributeNames": expression_names})
    try:
        success = await dynamodb_ops.update_item(AUTHZ_TABLE, update_attrs)
    except ClientError as ex:
        print(f"- ERROR: {ex}")
    return success


async def process_user(user: Dict[str, str], new_role: str) -> bool:
    success = False
    if PROD:
        success = await update(
            user["subject"],
            user["object"],
            {
                "role": f"{new_role}",
            },
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

    await migrate_roles(analyst_users, "analyst", "hacker")
    await migrate_roles(closer_users, "closer", "reattacker")
    await migrate_roles(gm_users, "group_manager", "system_owner")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
