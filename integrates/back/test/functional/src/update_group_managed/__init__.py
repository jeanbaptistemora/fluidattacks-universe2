# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def put_mutation(
    *,
    user: str,
    group: str,
    managed: str,
    comments: str,
) -> dict[str, Any]:
    query: str = """
        mutation UpdateGroupManaged (
            $comments: String!
            $groupName: String!
            $managed: ManagedType!
        ) {
            updateGroupManaged(
                comments: $comments
                groupName: $groupName
                managed: $managed
            ) {
                success
            }
        }
    """
    variables: dict[str, Any] = {
        "comments": comments,
        "groupName": group,
        "managed": managed,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
