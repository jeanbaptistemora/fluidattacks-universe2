# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration removes the date attribute for a group invitation
in the project access table

Execution Time:    2021-02-17 at 15:48:11 UTC-05
Finalization Time: 2021-02-17 at 15:48:30 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_types import (
    ProjectAccess as ProjectAccessType,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from group_access import (
    domain as group_access_domain,
)
from pprint import (
    pprint,
)
from typing import (
    cast,
)

TABLE_ACCESS_NAME = "FI_project_access"


async def remove_group_invitation_date(
    project_access: ProjectAccessType,
) -> bool:
    success = True
    user_email = project_access["user_email"]
    group_name = project_access["project_name"]
    invitation = project_access["invitation"]
    new_invitation = invitation.copy()

    if new_invitation.get("date"):
        del new_invitation["date"]

    success = cast(
        bool,
        await group_access_domain.update_legacy(
            user_email, group_name, {"invitation": new_invitation}
        ),
    )
    print("project_access")
    pprint(project_access)
    print("new_invitation")
    pprint(new_invitation)

    return success


async def main() -> None:
    scan_attrs = {
        "FilterExpression": (Attr("invitation").exists()),
    }
    project_accesses = await dynamodb_ops.scan(TABLE_ACCESS_NAME, scan_attrs)

    success = all(
        await collect(
            [
                remove_group_invitation_date(project_access)
                for project_access in project_accesses
            ],
            workers=64,
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
