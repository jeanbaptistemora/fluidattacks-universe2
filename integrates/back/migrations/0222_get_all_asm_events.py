# type: ignore

# pylint: disable=invalid-name,import-error
"""
Retrieve all events in active groups.

Execution Time:    2022-06-02 at 23:29:41 UTC
Finalization Time: 2022-06-02 at 23:46:31 UTC
"""

from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from events.dal import (
    list_group_events,
)
from itertools import (
    chain,
)
from newutils import (
    groups as groups_utils,
)
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    Any,
)


async def process_group(
    loaders: Dataloaders, group: Group
) -> list[dict[str, str]]:
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    event_ids = await list_group_events(group.name)
    group_events: list[dict[str, Any]] = await loaders.event.load_many(
        event_ids
    )

    return [
        {
            "organization_id": organization.id,
            "organization_name": organization.name,
            "group_name": group.name,
            "event_id": event["id"],
            "event_type": event["event_type"],
            "description": event["detail"],
            "event_status": event["event_status"],
            "closing_date": event["closing_date"],
        }
        for event in group_events
    ]


async def main() -> None:
    loaders: Dataloaders = get_new_context()

    active_groups = []
    async for org_id, _ in orgs_domain.iterate_organizations_legacy():
        org_groups = await loaders.organization_groups.load(org_id)
        org_active_groups = list(
            groups_utils.filter_active_groups(tuple(org_groups))
        )
        active_groups.extend(org_active_groups)

    results = list(
        chain.from_iterable(
            await collect(
                tuple(
                    process_group(loaders=loaders, group=group)
                    for group in active_groups
                ),
                workers=2,
            )
        )
    )

    csv_columns = [
        "organization_id",
        "organization_name",
        "group_name",
        "event_id",
        "event_type",
        "description",
        "event_status",
        "closing_date",
    ]
    csv_file = "0222_get_all_asm_events.csv"
    try:
        with open(csv_file, "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for data in results:
                writer.writerow(data)
    except IOError:
        print("   === I/O error")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
