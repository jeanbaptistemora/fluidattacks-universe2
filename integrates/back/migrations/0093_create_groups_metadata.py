# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name
# create all groups metadata if the group is active
#
# Execution time: Fri Jun 18 12:15:07 -05 2021
# Finalization time: Fri Jun 18 12:17:45 -05 2021

import aioextensions
from boto3.dynamodb.conditions import (
    Attr,
)
from contextlib import (
    suppress,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from dynamodb.model import (
    create_group_metadata,
)
from dynamodb.types import (
    GroupMetadata,
)

TABLE_NAME: str = "FI_projects"


@aioextensions.run_decorator
async def main() -> None:
    filtering_exp = Attr("project_status").eq("ACTIVE")
    query_attrs = {
        "ProjectionExpression": "#name,#language,#description",
        "FilterExpression": filtering_exp,
        "ExpressionAttributeNames": {
            "#name": "project_name",
            "#language": "language",
            "#description": "description",
        },
    }
    response = await dynamodb_ops.scan(TABLE_NAME, query_attrs)
    for group in response:
        print(f"[INFO] processing {group['project_name']}")
        with suppress(Exception):
            await create_group_metadata(
                group_metadata=GroupMetadata(
                    name=group["project_name"],
                    language=group["language"],
                    description=group["description"],
                )
            )


main()
