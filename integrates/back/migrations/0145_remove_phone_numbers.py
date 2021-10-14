# pylint: disable=invalid-name
"""
This migration wipes phone number user data from the DB

Execution Time:
Finalization Time:
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
    Any,
    cast,
    Collection,
    Dict,
    List,
    Type,
    Union,
)

# Constants
PROD: bool = False

USERS_TABLE: str = "fi_users"


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
    # pylint: disable=using-constant-test
    success = False
    set_expression = ""
    remove_expression = ""
    expression_names = {}
    expression_values = Dict[str, Collection[str]]
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

    update_attrs: Dict[
        str, Union[Type[Dict[Any, Any]], Dict[str, str], str]
    ] = {
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


async def migrate_users(users: List[UserType]) -> None:
    success = all(await collect(process_user(user) for user in users))
    print(f"Phone numbers removed: {success}")


async def main() -> None:
    users = await get_all_users()

    await migrate_users(users)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
