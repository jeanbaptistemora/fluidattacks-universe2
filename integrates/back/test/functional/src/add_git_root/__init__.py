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
    group: str,
) -> Dict[str, Any]:
    query: str = f"""
      mutation {{
        addGitRoot(
          branch: "master"
          credentials: {{
            key: "VGVzdCBTU0ggS2V5Cg=="
            name: "SSH Key"
            type: SSH
          }}
          environment: "production"
          gitignore: []
          groupName: "{group}"
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/test1"
        ) {{
          rootId
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
