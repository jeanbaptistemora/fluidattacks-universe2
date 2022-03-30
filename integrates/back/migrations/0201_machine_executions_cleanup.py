# pylint: disable=invalid-name
"""
This migration removes the items previously used to store machine executions
as the approach changed and they are no longer needed

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
from groups import (
    dal as groups_dal,
)
import logging
from settings import (
    LOGGING,
)
import time
from typing import (
    List,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


index = TABLE.indexes["inverted_index"]
key_structure = index.primary_key


async def process_group(group_name: str, progress: float) -> None:
    response = await operations.query(
        condition_expression=(
            Key("sk").eq(f"GROUP#{group_name}")
            & Key("pk").begins_with("ROOT#")
        ),
        facets=tuple(),
        index=index,
        table=TABLE,
    )
    keys = tuple(
        PrimaryKey(partition_key=item["pk"], sort_key=item["sk"])
        for item in response.items
        if "#MACHINE" in item["pk"]
    )

    await operations.batch_delete_item(
        keys=keys,
        table=TABLE,
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "keys": len(keys),
                "progress": str(progress),
            }
        },
    )


async def get_group_names() -> List[str]:
    return sorted(
        group["project_name"] for group in await groups_dal.get_all()
    )


async def main() -> None:
    groups = await get_group_names()

    await collect(
        tuple(
            process_group(group_name, count / len(groups))
            for count, group_name in enumerate(groups)
        ),
        workers=10,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
