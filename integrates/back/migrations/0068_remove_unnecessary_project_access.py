# pylint: disable=invalid-name
"""
This migration remove that project access for that user that
has not access to the group or is no pending to accept an invitation

Execution Time:    2021-02-04 at 14:12:40 UTC-05
Finalization Time: 2021-02-04 at 14:12:55 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    get_new_context,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from group_access import (
    domain as group_access_domain,
)

ACCESS_TABLE_NAME = "FI_project_access"


async def main() -> None:
    scan_attrs = {
        "FilterExpression": (
            Attr("has_access").eq(False) & Attr("invitation").not_exists()
        ),
    }
    project_accesses = await dynamodb_ops.scan(ACCESS_TABLE_NAME, scan_attrs)

    print("project_accesses")
    print(project_accesses)

    success = all(
        await collect(
            [
                group_access_domain.remove_access(
                    get_new_context(),
                    project_access["user_email"],
                    project_access["project_name"],
                )
                for project_access in project_accesses
            ],
            workers=64,
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
