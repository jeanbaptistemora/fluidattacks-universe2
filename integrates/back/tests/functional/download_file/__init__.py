# Standard libraries
from typing import (
    Any,
    Dict,
)

# Local libraries
from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def query(
    *,
    user: str,
    group: str,
    f_name: str,
) -> Dict[str, Any]:
    query: str = f"""
        mutation {{
            downloadFile (
                filesData: \"\\\"{f_name}\\\"\",
                projectName: "{group}"
            ) {{
                success
                url
            }}
        }}
    """
    data: Dict[str, str] = {
        'query': query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
