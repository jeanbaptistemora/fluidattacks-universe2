# type: ignore

# pylint: disable=invalid-name
"""
Migrate org info to "integrates_vms" table.
This migration does not include the org user access in "fi_organizations".

Execution Time:    2022-06-09 at 03:19:05 UTC
Finalization Time: 2022-06-09 at 03:23:41 UTC
"""

from aioextensions import (
    run,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model import (
    organizations as orgs_model,
    TABLE,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.types import (
    Policies,
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
    organizations as orgs_utils,
)
from organizations import (
    dal as orgs_dal,
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import simplejson as json
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


def adjust_historic_dates(
    historic: tuple[OrganizationState, ...] | tuple[Policies, ...],
) -> tuple[OrganizationState, ...] | tuple[Policies, ...]:
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


async def update_historic_policies(
    *,
    organization_id: str,
    historic: tuple[Policies, ...],
) -> None:
    organization_id = orgs_utils.remove_org_id_prefix(organization_id)
    key_structure = TABLE.primary_key
    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["organization_historic_policies"],
            values={
                "id": organization_id,
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


async def update_historic_state(
    *,
    organization_id: str,
    historic: tuple[OrganizationState, ...],
) -> None:
    organization_id = orgs_utils.remove_org_id_prefix(organization_id)
    key_structure = TABLE.primary_key
    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["organization_historic_state"],
            values={
                "id": organization_id,
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


async def process_organization(
    *,
    organization: Organization,
) -> None:
    organization_item: Item = await orgs_dal.get_by_name(organization.name)
    historic_policies = adjust_historic_dates(
        orgs_utils.format_historic_policies(organization_item)
    )
    historic_state = adjust_historic_dates(
        orgs_utils.format_historic_state(organization_item)
    )

    await update_historic_policies(
        organization_id=organization.id, historic=historic_policies
    )
    await update_historic_state(
        organization_id=organization.id, historic=historic_state
    )
    await orgs_model.add(organization=organization)

    LOGGER_CONSOLE.info(
        "Organization processed",
        extra={
            "extra": {
                "org_id": organization.id,
                "org_name": organization.name,
            }
        },
    )


async def main() -> None:
    all_org_names: list[str] = []
    async for organization in orgs_domain.iterate_organizations():
        all_org_names.append(organization.name)
        await process_organization(organization=organization)

    LOGGER_CONSOLE.info(
        "All organizations", extra={"extra": {"processed": len(all_org_names)}}
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
