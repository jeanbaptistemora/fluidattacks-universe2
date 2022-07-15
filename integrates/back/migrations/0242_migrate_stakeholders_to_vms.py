# pylint: disable=invalid-name
"""
Migrate stakeholders metadata to "integrates_vms" table.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from db_model.stakeholders.constants import (
    ALL_STAKEHOLDERS_INDEX_METADATA,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.stakeholders.utils import (
    format_stakeholder_item,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils import (
    stakeholders as stakeholders_utils,
)
from settings import (
    LOGGING,
)
from stakeholders import (
    dal as stakeholders_dal,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def add(*, stakeholder: Stakeholder) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={
            "email": stakeholder.email,
        },
    )
    gsi_2_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={
            "all": "all",
            "email": stakeholder.email,
        },
    )
    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        **format_stakeholder_item(stakeholder),
    }

    await operations.put_item(
        facet=TABLE.facets["stakeholder_metadata"],
        item=item,
        table=TABLE,
    )


async def format_stakeholder(item_legacy: Item) -> Stakeholder:
    # We need to check vms for the stakeholder's notification preferences
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": item_legacy["email"]},
    )
    item_vms = await operations.get_item(
        facets=(TABLE.facets["stakeholder_metadata"],),
        key=primary_key,
        table=TABLE,
    )

    return stakeholders_utils.format_stakeholder(item_legacy, item_vms)


async def process_stakeholder(stakeholder_item: Item) -> None:
    stakeholder: Stakeholder = await format_stakeholder(stakeholder_item)
    await add(stakeholder=stakeholder)
    LOGGER_CONSOLE.info(
        "Processed",
        extra={"extra": {"email": stakeholder.email}},
    )


async def main() -> None:
    stakeholders_scanned: list[Item] = await stakeholders_dal.get_all(
        filter_exp=Attr("email").exists()
    )

    LOGGER_CONSOLE.info(
        "All stakeholders",
        extra={"extra": {"scanned": len(stakeholders_scanned)}},
    )

    await collect(
        tuple(process_stakeholder(item) for item in stakeholders_scanned),
        workers=8,
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
