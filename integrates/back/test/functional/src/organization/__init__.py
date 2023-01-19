# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Optional,
)


async def get_result(
    *,
    user: str,
    org: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            organization(organizationId: "{org}") {{
                id
                company {{
                    domain
                    trial {{
                        completed
                    }}
                }}
                coveredAuthors
                coveredCommits
                coveredRepositories
                missedAuthors
                missedCommits
                missedRepositories
                inactivityPeriod
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptances
                minAcceptanceSeverity
                minBreakingSeverity
                name
                groups {{
                    name
                }}
                integrationRepositoriesConnection(first: 100) {{
                    __typename
                    edges {{
                        node {{
                            defaultBranch
                            lastCommitDate
                            url
                        }}
                    }}
                    pageInfo {{
                        hasNextPage
                        endCursor
                    }}
                }}
                stakeholders {{
                    email
                }}
                credentials {{
                    azureOrganization
                    isPat
                    name
                    type
                }}
                permissions
                userRole
                vulnerabilityGracePeriod
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_vulnerabilities_url(
    *,
    user: str,
    org_id: str,
    verification_code: Optional[str] = None,
    session_jwt: Optional[str] = None,
) -> dict[str, Any]:
    query: str = """
        query GetOrgVulnerabilitiesUrl(
            $orgId: String!
            $verificationCode: String
        ) {
            organization(organizationId: $orgId) {
                name
                vulnerabilitiesUrl(verificationCode: $verificationCode)
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "orgId": org_id,
            "verificationCode": verification_code,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
        session_jwt=session_jwt,
    )
