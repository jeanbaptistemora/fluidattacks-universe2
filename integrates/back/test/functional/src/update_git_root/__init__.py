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


async def get_result_1(
    *,
    user: str,
    group: str,
    credential_key: str,
    credential_name: str,
) -> Dict[str, Any]:
    query: str = f"""
      mutation UpdateGitRoot(
            $credentialKey: String!, $credentialName: String!
        ) {{
        updateGitRoot(
            branch: "develop"
            credentials: {{
                key: $credentialKey
                name: $credentialName
                type: SSH
            }}
            environment: "QA"
            gitignore: ["node_modules/"]
            groupName: "{group}"
            id: "88637616-41d4-4242-854a-db8ff7fe1ab6"
            includesHealthCheck: false
            url: "https://gitlab.com/fluidattacks/nickname"
        ) {{
            success
        }}
      }}
    """
    variables: dict[str, str] = {
        "credentialKey": credential_key,
        "credentialName": credential_name,
    }
    data = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
