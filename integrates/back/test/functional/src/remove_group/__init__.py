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


async def get_result(
    *,
    user: str,
    group: str,
    reason: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            removeGroup(
                groupName: "{group}"
                reason: {reason}
            ) {{
            success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_query_group(
    *,
    email: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            group(groupName: "{group_name}"){{
                name
                __typename
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
