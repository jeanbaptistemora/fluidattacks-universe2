# type: ignore

# pylint: disable=invalid-name
"""
Remove empty attributes from credentials

Execution Time:    2022-04-29 at 14:59:10 UTCUTC
Finalization Time: 2022-04-29 at 15:00:31 UTCUTC
"""

from aioboto3.dynamodb.table import (
    CustomTableResource,
)
from aioextensions import (
    run,
)
import asyncio
from db_model.credentials.get import (
    get_credentials,
)
from db_model.credentials.types import (
    CredentialItem,
)
from dynamodb.resource import (
    get_resource,
)
from groups.dal import (  # pylint: disable=import-error
    get_active_groups,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def main() -> None:
    groups = await get_active_groups()
    resource = await get_resource()
    table_resource: CustomTableResource = await resource.Table(
        "integrates_vms"
    )

    for result in asyncio.as_completed(
        [get_credentials(group_name=group) for group in groups]
    ):
        credentials: tuple[CredentialItem, ...] = await result
        if not credentials:
            continue
        for cred in credentials:
            if (
                cred.state.key == ""
                or cred.state.user == ""
                or cred.state.password == ""
                or cred.state.token == ""
            ):
                print(cred.id)
                attrs_to_remove = []
                expression_attrs = {}
                if cred.state.key == "":
                    attrs_to_remove.append("#key")
                    expression_attrs["#key"] = "key"
                if cred.state.user == "":
                    attrs_to_remove.append("#user")
                    expression_attrs["#user"] = "user"
                if cred.state.password == "":
                    attrs_to_remove.append("#password")
                    expression_attrs["#password"] = "password"
                if cred.state.token == "":
                    attrs_to_remove.append("#token")
                    expression_attrs["#token"] = "token"

                update_expresion = f" REMOVE {', '.join(attrs_to_remove)}"
                expression = {
                    "Key": {
                        "pk": f"CRED#{cred.id}",
                        "sk": f"STATE#{cred.state.modified_date}",
                    },
                    "UpdateExpression": update_expresion,
                    "ExpressionAttributeNames": expression_attrs,
                }

                await table_resource.update_item(**expression)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
