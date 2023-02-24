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
    email: str,
    role: str,
) -> dict[str, Any]:
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
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder="admin@gmail.com",
        context=get_new_context(),
    )
