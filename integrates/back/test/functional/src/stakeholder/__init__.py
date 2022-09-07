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
    stakeholder: str,
    group: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            stakeholder(entity: GROUP,
                    groupName: "{group}",
                    userEmail: "{stakeholder}") {{
                email
                firstLogin
                groups {{
                    name
                }}
                invitationState
                lastLogin
                responsibility
                role
                __typename
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
