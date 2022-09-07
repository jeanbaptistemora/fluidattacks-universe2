# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
Migrate groups to "integrates_vms" table.

Execution Time:    2022-05-26 at 02:20:18 UTC
Finalization Time: 2022-05-26 at 02:36:49 UTC
"""

from aioextensions import (
    collect,
    run,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model import (
    groups as groups_model,
    TABLE,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from dynamodb import (
    keys,
    operations,
)
import dynamodb.operations_legacy as ops_legacy
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils import (
    groups as groups_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import simplejson as json  # type: ignore
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

PROJECTS_TABLE: str = "FI_projects"


def adjust_historic_dates(
    historic: tuple[GroupState, ...],
) -> tuple[GroupState, ...]:
    """Ensure dates are not the same and in ascending order."""
    new_historic = []
    comparison_date = ""
    for entry in historic:
        if entry.modified_date > comparison_date:
            comparison_date = entry.modified_date
        else:
            fixed_date = datetime.fromisoformat(comparison_date) + timedelta(
                seconds=1
            )
            comparison_date = fixed_date.astimezone(
                tz=timezone.utc
            ).isoformat()
        new_historic.append(entry._replace(modified_date=comparison_date))
    return tuple(new_historic)


async def update_historic_state(
    *,
    group_name: str,
    historic: tuple[GroupState, ...],
) -> None:
    key_structure = TABLE.primary_key
    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["group_historic_state"],
            values={
                "name": group_name,
                "iso8601utc": entry.modified_date,
            },
        )
        for entry in historic
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(entry)),
        }
        for key, entry in zip(new_keys, historic)
    )
    await operations.batch_put_item(items=new_items, table=TABLE)


async def process_group(
    *,
    group_item: Item,
    progress: float,
) -> None:
    group_name = get_key_or_fallback(group_item)
    organization_id = await orgs_domain.get_id_for_group(group_name)
    if organization_id == "":
        organization_id = "ORG#unknown"

    group: Group = groups_utils.format_group(
        item=group_item, organization_id=organization_id
    )
    await groups_model.add(group=group)

    historic_state = adjust_historic_dates(
        groups_utils.format_group_historic_state(group_item)
    )
    await update_historic_state(group_name=group_name, historic=historic_state)

    indicators = groups_utils.format_group_unreliable_indicators(group_item)
    await groups_model.update_unreliable_indicators(
        group_name=group_name, indicators=indicators
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    groups_scanned: list[Item] = await ops_legacy.scan(
        table=PROJECTS_TABLE,
        scan_attrs={},
    )
    LOGGER_CONSOLE.info(
        "All groups",
        extra={
            "extra": {
                "groups_to_migrate": len(groups_scanned),
            }
        },
    )

    await collect(
        tuple(
            process_group(
                group_item=item, progress=count / len(groups_scanned)
            )
            for count, item in enumerate(groups_scanned)
        ),
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
