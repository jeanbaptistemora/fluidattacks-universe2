# pylint: disable=import-error
from back.tests.functional.utils import (
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
    responsibility: str,
    role: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            grantStakeholderAccess (
                email: "{stakeholder}"
                groupName: "{group}"
                responsibility: "{responsibility}"
                role: {role}
            ) {{
            success
                grantedStakeholder {{
                    email
                }}
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


async def get_stakeholders(
    *,
    user: str,
    group: str,
) -> dict[str, Any]:
    query: str = """
        query GetStakeholders($groupName: String!) {
            group (groupName: $groupName) {
                stakeholders {
                    email
                    invitationState
                }
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "groupName": group,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
