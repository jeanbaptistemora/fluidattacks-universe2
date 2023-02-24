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
    organization_id: str,
    credentials_id: str,
    credentials: dict,
) -> dict[str, Any]:
    query: str = """
        mutation UpdateCredentialsMutation(
            $organizationId: ID!,
            $credentialsId: ID!,
            $credentials: CredentialsInput!
        ) {
            updateCredentials(
                organizationId: $organizationId
                credentialsId: $credentialsId
                credentials: $credentials
            ) {
                success
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "organizationId": organization_id,
            "credentialsId": credentials_id,
            "credentials": credentials,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
