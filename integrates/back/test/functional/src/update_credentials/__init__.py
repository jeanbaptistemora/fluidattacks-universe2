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
    user: str,
    organization_id: str,
    credentials_id: str,
    credentials: dict,
) -> Dict[str, Any]:
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
    data: Dict[str, Any] = {
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
