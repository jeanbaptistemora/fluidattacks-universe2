# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration add expiration_time to project access for that stakeholder
who has not confirmed the group invitation

Execution Time:    2021-02-16 at 16:52:25 UTC-05
Finalization Time: 2021-02-16 at 16:52:36 UTC-05
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
from newutils import (
    datetime as datetime_utils,
)
from pprint import (
    pprint,
)
from typing import (
    cast,
)

TABLE_ACCESS_NAME = "FI_project_access"


async def add_expiration_time_to_project_access(
    project_access: ProjectAccessType,
) -> bool:
    success = True
    user_email = project_access["user_email"]
    group_name = project_access["project_name"]
    invitation = project_access["invitation"]
    expiration_time = datetime_utils.get_as_epoch(
        datetime_utils.get_plus_delta(
            datetime_utils.get_from_str(invitation["date"]), weeks=1
        )
    )

    success = cast(
        bool,
        await group_access_domain.update_legacy(
            user_email, group_name, {"expiration_time": expiration_time}
        ),
    )
    print("project_access")
    pprint(project_access)
    print("expiration_time")
    pprint(expiration_time)

    return success


async def main() -> None:
    scan_attrs = {
        "FilterExpression": (
            Attr("invitation").exists() & Attr("invitation.is_used").eq(False)
        ),
    }
    project_accesses = await dynamodb_ops.scan(TABLE_ACCESS_NAME, scan_attrs)

    success = all(
        await collect(
            [
                add_expiration_time_to_project_access(project_access)
                for project_access in project_accesses
            ],
            workers=64,
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
