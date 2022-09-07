# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration swaps all customeradmins for user_managers and customers for
users

Execution Time:    2022-02-10 at 14:45:23 UTC-5
Finalization Time: 2022-02-10 at 14:47:26 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from aiohttp.client_exceptions import (
    ClientError,
)
from boto3.dynamodb.conditions import (
    Attr,
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
    role: str = "",
    data_attr: str = "",
) -> List[UserType]:
    filtering_exp: object = ""
    if role:
        filtering_exp = Attr("role").eq(role)
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


async def process_user(user: Dict[str, str], to_role: str) -> bool:
    success = False
    if PROD:
        success = await update(
            user["subject"],
            user["object"],
            {
                "role": f"{to_role}",
            },
        )
    return success


async def migrate_users(users: List[UserType], to_role: str) -> None:
    success = all(await collect(process_user(user, to_role) for user in users))
    print(f"Customers migrated: {success}")


async def main() -> None:
    customeradmins = await get_all_users(role="customeradmin")
    await migrate_users(customeradmins, to_role="user_manager")

    customers = await get_all_users(role="customer")
    await migrate_users(customers, to_role="user")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
