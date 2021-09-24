# pylint: disable=invalid-name
"""
This migration removes the hasRelease field from groups
since it is not used

Execution Time:    2021-09-24 at 13:34:17 UTC-5
Finalization Time: 2021-09-24 at 13:34:38 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_types import (
    Group,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from groups import (
    dal as groups_dal,
)

GROUP_TABLE = "FI_projects"


async def remove_has_release_field_from_group(group: Group) -> bool:
    success = await groups_dal.update(
        group["project_name"], {"hasRelease": None}
    )
    print(f'Removed hasRelease from {group["project_name"]}')
    return success


async def main() -> None:
    scan_attrs = {
        "FilterExpression": Attr("hasRelease").exists(),
        "ProjectionExpression": ",".join({"project_name"}),
    }
    groups = await dynamodb_ops.scan(GROUP_TABLE, scan_attrs)

    success = all(
        await collect(
            [remove_has_release_field_from_group(group) for group in groups]
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
