# pylint: disable=invalid-name
"""
This migration aims to apply standardization to organization
finding policies names

Execution Time:    2021-08-19 at 06:31:14 UTC-05
Finalization Time: 2021-08-19 at 06:31:25 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
import csv
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
)
from organizations.domain import (
    iterate_organizations,
)
from organizations_finding_policies.dal import (
    get_organization_finding_policies,
)
import time
from typing import (
    Dict,
    List,
    Tuple,
)

# Constants
PROD: bool = True


async def update_organization_finding_policy_metadata(
    *,
    old_finding_name: str,
    organization_name: str,
    finding_policy_id: str,
    finding_policy_metadata: OrgFindingPolicyMetadata,
) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": organization_name, "uuid": finding_policy_id},
    )
    metadata_item = dict(finding_policy_metadata._asdict())

    condition_expression = Attr(key_structure.partition_key).exists()
    print(
        "Updating policy metadata",
        finding_policy_id,
        finding_policy_metadata.name,
        old_finding_name,
    )
    if PROD:
        await operations.update_item(
            condition_expression=condition_expression,
            item=metadata_item,
            key=metadata_key,
            table=TABLE,
        )


async def update_organization_findings_policies(
    *, name: str, typologies_migration: Dict[str, str]
) -> None:
    policies: Tuple[
        OrgFindingPolicyItem, ...
    ] = await get_organization_finding_policies(org_name=name)

    for policy in policies:
        if policy.metadata.name.strip() in typologies_migration.keys():
            await update_organization_finding_policy_metadata(
                old_finding_name=policy.metadata.name.strip(),
                organization_name=policy.org_name,
                finding_policy_id=policy.id,
                finding_policy_metadata=OrgFindingPolicyMetadata(
                    name=typologies_migration[
                        policy.metadata.name.strip()
                    ].strip(),
                    tags=policy.metadata.tags,
                ),
            )


async def main() -> None:
    organizations_names: List[str] = []

    async for _, org_name in iterate_organizations():
        organizations_names.append(org_name)

    with open("0102_findings_titles.csv", mode="r", encoding="utf8") as infile:
        reader = csv.reader(infile)
        typologies_migration = {rows[0]: rows[1] for rows in reader}

    await collect(
        [
            update_organization_findings_policies(
                name=organization_name,
                typologies_migration=typologies_migration,
            )
            for organization_name in organizations_names
        ],
        workers=24,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
