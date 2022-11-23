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
    granting_email: str,
    group: str,
    modified_email: str,
    modified_role: str,
    responsibility: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            updateGroupStakeholder (
                email: "{modified_email}"
                groupName: "{group}"
                responsibility: "{responsibility}"
                role: {modified_role}
            ) {{
                success
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=granting_email,
        context=get_new_context(),
    )
