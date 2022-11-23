# pylint: disable=invalid-name
"""
remove notification preferences field from stakeholder_metadata

Execution Time:    2022-11-01 at 20:42:00 UTC
Finalization Time: 2022-11-01 at 20:42:52 UTC
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
from db_model.stakeholders import (
    get_all_stakeholders,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from dynamodb import (
    keys,
    operations,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def remove_notification(
    *,
    email: str,
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={
            "email": email,
        },
    )
    item = {"notifications_preferences": None}
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=item,
        key=primary_key,
        table=TABLE,
    )


async def process_user(user: Stakeholder, progress: float) -> None:
    await remove_notification(
        email=user.email.strip().lower(),
    )
    LOGGER_CONSOLE.info(
        "User processed",
        extra={
            "extra": {
                "user email": user.email,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    all_stakeholders = await get_all_stakeholders()
    LOGGER_CONSOLE.info(
        "Active users",
        extra={"extra": {"users_len": len(all_stakeholders)}},
    )
    await collect(
        tuple(
            process_user(
                user=stakeholder, progress=count / len(all_stakeholders)
            )
            for count, stakeholder in enumerate(all_stakeholders)
        ),
        workers=16,
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
