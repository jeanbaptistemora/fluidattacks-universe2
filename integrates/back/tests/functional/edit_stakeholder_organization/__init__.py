# Standard libraries
import json
import os
from typing import (
    Any,
    Dict,
)

# Local libraries
from backend.api import (
    get_new_context,
)
from back.tests.functional.utils import (
    get_graphql_result,
)


async def query(
    *,
    user: str,
    org: str,
    email: str,
    role: str,
    phone: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            editStakeholderOrganization(
                organizationId: "{org}",
                userEmail: "{email}",
                phoneNumber: "{phone}",
                role: {role}
            ) {{
                success
                modifiedStakeholder {{
                    email
                }}
            }}
        }}
    """
    data: Dict[str, Any] = {
        'query': query
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
