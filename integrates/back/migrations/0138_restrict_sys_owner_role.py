# pylint: disable=invalid-name
"""
This migration swaps all non-fuid staff system owners to user managers

Execution Time:    2021-09-22 at 18:02:01 UTC-5
Finalization Time: 2021-09-22 at 18:02:10 UTC-5
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
from users.domain import (
    is_fluid_staff,
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


async def process_user(user: Dict[str, str]) -> bool:
    success = False
    if PROD:
        success = await update(
            user["subject"],
            user["object"],
            {
                "role": "customeradmin",
            },
        )
    return success


async def migrate_users(users: List[UserType]) -> None:
    success = all(await collect(process_user(user) for user in users))
    print(f"Non Fluid system owners migrated: {success}")


async def main() -> None:
    authz_users = await get_all_users()

    so_users = [
        user
        for user in authz_users
        if user.get("role", "") == "system_owner"
        and not is_fluid_staff(user.get("subject", ""))
    ]

    await migrate_users(so_users)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
