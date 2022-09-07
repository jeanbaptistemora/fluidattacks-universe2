# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration wipes phone number user data from the DB

Execution Time:    2021-10-14 at 13:11:25 UTC-5
Finalization Time: 2021-10-14 at 13:13:27 UTC-5
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

USERS_TABLE: str = "FI_users"


async def get_all_users(
    filtering_exp: object = "",
    data_attr: str = "",
) -> List[UserType]:
    scan_attrs = {}
    if filtering_exp:
        scan_attrs["FilterExpression"] = filtering_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(USERS_TABLE, scan_attrs)
    return cast(List[UserType], items)


async def update(email: str, data: Dict[str, None]) -> bool:
    """Manually updates db data"""
    success = False
    set_expression = ""
    remove_expression = ""
    expression_names = {}
    expression_values = {}  # type: ignore
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
            "email": email,
        },
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    if expression_names:
        update_attrs.update({"ExpressionAttributeNames": expression_names})
    try:
        success = await dynamodb_ops.update_item(USERS_TABLE, update_attrs)
    except ClientError as ex:
        print(f"- ERROR: {ex}")
    return success


async def process_user(user: Dict[str, str]) -> bool:
    success = False
    if PROD:
        success = await update(
            user["email"],
            {"phone": None},
        )
    return success


async def remove_phones(users: List[UserType]) -> None:
    success = all(await collect(process_user(user) for user in users))
    print(f"Phone numbers removed: {success}")


async def main() -> None:
    users = await get_all_users()
    await remove_phones(users)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
