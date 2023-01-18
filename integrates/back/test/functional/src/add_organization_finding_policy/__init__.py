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
    organization_name: str,
    finding_name: str,
) -> dict[str, Any]:
    mutation: str = f"""
        mutation {{
            addOrganizationFindingPolicy(
                findingName: "{finding_name}",
                organizationName: "{organization_name}",
            ) {{
                success
            }}
        }}
    """
    data = {"query": mutation}

    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
