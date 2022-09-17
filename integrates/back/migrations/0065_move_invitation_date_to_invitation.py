# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name
"""
This migration move the attribute invitation_date of project_access table
to the field invitation of the same table

Execution Time:    2021-01-29 at 16:45:07 UTC-05
Finalization Time: 2021-01-29 at 16:45:24 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import authz
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_types import (  # pylint: disable=import-error
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


async def move_invitation_date_to_invitation(
    project_access: ProjectAccessType,
) -> bool:
    invitation_date = project_access["invitation_date"]
    user_email = project_access["user_email"]
    group_name = project_access["project_name"]
    responsibility = project_access["responsibility"]
    is_used = project_access["has_access"]
    group_role = await authz.get_group_level_role_legacy(
        user_email, group_name
    )
    url_token = "unknown"  # nosec
    new_invitation = {
        "date": invitation_date,
        "is_used": is_used,
        "responsibility": responsibility,
        "role": group_role,
        "url_token": url_token,
    }
    print("project_access")
    pprint(project_access)
    print("new_invitation")
    pprint(new_invitation)

    success = cast(
        bool,
        await group_access_domain.update_legacy(
            user_email,
            group_name,
            {"invitation": new_invitation, "invitation_date": None},
        ),
    )

    return success


async def main() -> None:
    scan_attrs = {
        "FilterExpression": (Attr("invitation_date").exists()),
    }
    project_accesses = await dynamodb_ops.scan(TABLE_ACCESS_NAME, scan_attrs)

    success = all(
        await collect(
            [
                move_invitation_date_to_invitation(project_access)
                for project_access in project_accesses
            ],
            workers=64,
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
