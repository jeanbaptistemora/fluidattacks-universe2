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
    email: str,
    role: str,
) -> Dict[str, Any]:
    query = f"""
        mutation {{
            addStakeholder(
                email: "{email}",
                role: {role}
            ) {{
                success
                email
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder="admin@gmail.com",
        context=get_new_context(),
    )
