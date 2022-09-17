# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name
"""
Migrate subscriptions to "integrates_vms" table.

Execution Time:    2022-09-08 at 03:25:45 UTC
Finalization Time: 2022-09-08 at 03:25:47 UTC
"""

from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    subscriptions as subscriptions_model,
)
from db_model.subscriptions.types import (
    Subscription,
)
from dynamodb import (
    operations_legacy as ops_legacy,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils.encodings import (
    key_to_mapping,
)
from newutils.subscriptions import (
    format_subscription,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
SUBSCRIPTIONS_TABLE = "fi_subscriptions"


def _unpack_item(item: Item) -> Item:
    return {
        **item,
        "pk": key_to_mapping(item["pk"]),
        "sk": key_to_mapping(item["sk"]),
    }


async def exists(loaders: Dataloaders, email: str) -> bool:
    try:
        await loaders.stakeholder.load(email)
        return True
    except StakeholderNotFound:
        return False


async def process_subscription(item: Item) -> None:
    loaders: Dataloaders = get_new_context()
    item = _unpack_item(item)
    email = item["pk"]["email"]
    if not await exists(loaders, email):
        return
    subscription: Subscription = format_subscription(item)
    await subscriptions_model.add(subscription=subscription)


async def main() -> None:
    subscriptions_scanned: list[Item] = await ops_legacy.scan(
        table=SUBSCRIPTIONS_TABLE, scan_attrs={}
    )
    LOGGER_CONSOLE.info(
        "All stakeholder subscriptions",
        extra={"extra": {"scanned": len(subscriptions_scanned)}},
    )

    await collect(
        tuple(process_subscription(item) for item in subscriptions_scanned),
        workers=256,
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
