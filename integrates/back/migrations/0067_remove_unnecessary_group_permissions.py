# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration remove the group level permission for stakeholders
that do not have group access

Execution Time:    2021-02-04 at 10:00:26 UTC-05
Finalization Time: 2021-02-04 at 10:01:03 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import authz
from boto3.dynamodb.conditions import (
    Attr,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)

ACCESS_TABLE_NAME = "FI_project_access"
AUTHZ_TABLE_NAME = "fi_authz"


async def main() -> None:
    scan_attrs = {
        "FilterExpression": (Attr("has_access").eq(True)),
    }
    project_accesses = await dynamodb_ops.scan(ACCESS_TABLE_NAME, scan_attrs)
    project_accesses = [
        (project_access["user_email"], project_access["project_name"])
        for project_access in project_accesses
    ]

    scan_attrs = {
        "FilterExpression": (Attr("level").eq("group")),
    }
    group_authzes = await dynamodb_ops.scan(AUTHZ_TABLE_NAME, scan_attrs)
    group_authzes = [
        (group_authz["subject"], group_authz["object"])
        for group_authz in group_authzes
    ]

    group_authzes_to_delete = [
        group_authz
        for group_authz in group_authzes
        if group_authz not in project_accesses
    ]

    print("group_authzes_to_delete")
    print(group_authzes_to_delete)

    success = all(
        await collect(
            [
                authz.revoke_group_level_role_legacy(email, group_name)
                for email, group_name in group_authzes_to_delete
            ],
            workers=64,
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
