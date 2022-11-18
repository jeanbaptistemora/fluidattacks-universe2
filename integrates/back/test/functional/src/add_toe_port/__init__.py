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
    Dict,
)


async def get_result(
    *,
    address: str,
    group_name: str,
    port: str,
    root_id: str,
    user: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            addToePort(
                address: "{address}",
                groupName: "{group_name}",
                port: {port},
                rootId: "{root_id}",
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )