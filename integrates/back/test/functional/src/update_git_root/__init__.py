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
    credential_id: str,
    credential_name: str,
) -> Dict[str, Any]:
    query: str = f"""
      mutation {{
        updateGitRoot(
            branch: "develop"
            credentials: {{
                id: "{credential_id}"
                name: "{credential_name}"
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
    data: Dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result_2(
    *, user: str, group: str, root_id: str, credential_id: str
) -> Dict[str, Any]:
    query: str = f"""
      mutation {{
        updateGitRoot(
            branch: "develop"
            credentials: {{
                id: "{credential_id}"
                key: "VGVzdCBTU0gK"
                name: "New SSH Key"
                type: SSH
            }}
            environment: "QA"
            gitignore: ["node_modules/"]
            groupName: "{group}"
            id: "{root_id}"
            includesHealthCheck: false
            url: "https://gitlab.com/fluidattacks/nickname2"
        ) {{
            success
        }}
      }}
    """
    data: Dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
