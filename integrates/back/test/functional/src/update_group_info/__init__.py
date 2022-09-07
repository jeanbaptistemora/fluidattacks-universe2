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
    business_id: str,
    business_name: str,
    user: str,
    group: str,
    description: str,
    language: str,
    sprint_duration: int,
    sprint_start_date: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateGroupInfo(
                businessId: "{business_id}"
                businessName: "{business_name}"
                description: "{description}"
                groupName: "{group}"
                language: {language}
                sprintDuration: {sprint_duration}
                sprintStartDate: "{sprint_start_date}"
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
