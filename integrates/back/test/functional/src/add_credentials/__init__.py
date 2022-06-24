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
    user: str,
    organization_id: str,
    credentials: dict[str, str],
) -> Dict[str, Any]:
    query: str = """
        mutation AddCredentialsMutation(
            $organizationId: ID!, $credentials: CredentialsInput!
        ) {
            addCredentials(
                organizationId: $organizationId
                credentials: $credentials
            ) {
                success
            }
        }
    """
    data: Dict[str, Any] = {
        "query": query,
        "variables": {
            "organizationId": organization_id,
            "credentials": credentials,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
