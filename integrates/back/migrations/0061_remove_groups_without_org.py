# pylint: disable=invalid-name
"""
This migration removes groups without an associated organization

Execution Time:    2021-01-21 at 09:25:39 UTC-05
Finalization Time: 2021-01-21 at 09:26:08 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from dataloaders import (
    get_new_context,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from groups import (
    domain as groups_domain,
)
from organizations import (
    dal as orgs_dal,
    domain as orgs_domain,
)
from typing import (
    cast,
)

FINDINGS_TABLE = "FI_findings"
ORG_TABLE = "fi_organizations"


async def remove_group(group_name: str, org_id: str) -> bool:
    context = get_new_context()
    email = "integrates@fluidattacks.com"
    success = await groups_domain.remove_group_legacy(
        context, group_name, email, org_id
    )
    print(f"{group_name} was removed")

    return success


async def remove_group_from_organization_table(
    org_id: str, group_name: str
) -> bool:
    success = cast(bool, await orgs_dal.remove_group(org_id, group_name))
    print(f"{group_name} was removed from org table")

    return success


async def main() -> None:
    projection_expression = ", ".join({"pk", "sk"})
    query_attrs = {
        "FilterExpression": (
            Key("pk").begins_with("ORG#") & Key("sk").begins_with("INFO#")
        ),
        "ProjectionExpression": projection_expression,
    }
    orgs = await dynamodb_ops.scan(ORG_TABLE, query_attrs)
    orgs_ids = [org["pk"] for org in orgs]

    # Remove alive groups that do not have associated org
    group_names = await groups_domain.get_alive_groups()
    group_org_ids = await collect(
        [
            orgs_domain.get_id_for_group(group_name)
            for group_name in group_names
        ],
        workers=64,
    )
    alive_groups_to_remove = list(
        filter(
            lambda group: group[1] not in orgs_ids,
            zip(group_names, group_org_ids),
        )
    )
    success = all(
        await collect(
            [
                remove_group(group_name, org_id)
                for group_name, org_id in alive_groups_to_remove
            ],
            workers=64,
        )
    )

    # Remove groups from organization table that do not have associated org
    query_attrs = {
        "FilterExpression": (
            Key("pk").begins_with("ORG#") & Key("sk").begins_with("GROUP#")
        ),
        "ProjectionExpression": projection_expression,
    }
    org_groups = await dynamodb_ops.scan(ORG_TABLE, query_attrs)
    org_groups_to_remove = list(
        filter(lambda group: group["pk"] not in orgs_ids, org_groups)
    )
    success = success and all(
        await collect(
            [
                remove_group_from_organization_table(
                    group["pk"], group["sk"].split("#")[1]
                )
                for group in org_groups_to_remove
            ],
            workers=64,
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
