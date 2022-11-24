# pylint: disable=invalid-name
"""
For organization finding policies, insert state info in metadata item
as it is done with other entities. Also delete unneeded item for facet
org_finding_policy_state.

Execution Time:    2022-11-22 at 18:10:15 UTC
Finalization Time: 2022-11-22 at 18:11:53 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from db_model import (
    TABLE,
)
from db_model.organizations.get import (
    get_all_organizations,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (  # type: ignore
    get_org_finding_policies,
)
from dynamodb.types import (  # type: ignore
    Item,
    OrgFindingPolicyItem,
    PrimaryKey,
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


async def _process_historic_item(item: Item) -> None:
    modified_item = item.copy()
    modified_item["sk"] = f'STATE#{item["modified_date"]}'
    await operations.put_item(
        facet=TABLE.facets["org_finding_policy_historic_state"],
        item=modified_item,
        table=TABLE,
    )
    await operations.delete_item(
        key=PrimaryKey(partition_key=item["pk"], sort_key=item["sk"]),
        table=TABLE,
    )


async def _process_org_finding_policy(
    finding_policy: OrgFindingPolicyItem,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": finding_policy.org_name, "uuid": finding_policy.id},
    )
    item = {
        "state": dict(finding_policy.state._asdict()),
    }
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=metadata_key,
        table=TABLE,
    )
    legacy_state_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_state"],
        values={
            "name": finding_policy.org_name,
            "uuid": finding_policy.id,
        },
    )
    await operations.delete_item(key=legacy_state_key, table=TABLE)

    historic_state_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"uuid": finding_policy.id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(
                historic_state_key.partition_key
            )
            & Key(key_structure.sort_key).begins_with("POLICY#")
        ),
        facets=(TABLE.facets["org_finding_policy_historic_state"],),
        table=TABLE,
    )
    historic_state_items = [
        item
        for item in response.items
        if str(item["sk"]).startswith("POLICY#") and "STATE#" in item["sk"]
    ]
    await collect(
        tuple(_process_historic_item(item) for item in historic_state_items),
        workers=4,
    )


async def _process_organization(
    org_name: str,
    progress: float,
) -> None:
    org_policies = await get_org_finding_policies(org_name=org_name)
    if not org_policies:
        return
    await collect(
        tuple(_process_org_finding_policy(policy) for policy in org_policies),
        workers=4,
    )
    LOGGER_CONSOLE.info(
        "Organization processed",
        extra={
            "extra": {
                "name": org_name,
                "policies": len(org_policies),
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    all_orgs = await get_all_organizations()
    all_org_names: list[str] = sorted([org.name for org in all_orgs])
    LOGGER_CONSOLE.info(
        "Orgs to process",
        extra={"extra": {"all_len": len(all_orgs)}},
    )
    await collect(
        tuple(
            _process_organization(
                org_name=org_name,
                progress=count / len(all_org_names),
            )
            for count, org_name in enumerate(all_org_names)
        ),
        workers=4,
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
