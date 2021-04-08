# Standard libraries
import json
import os
from typing import (
    Any,
    Dict,
    List,
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
    group: str,
    tags: List[str],
) -> Dict[str, Any]:
    query: str = """
        mutation AddTagsMutation($projectName: String!, $tagsData: JSONString!) {
            addTags (
                tags: $tagsData,
                projectName: $projectName) {
                success
            }
        }
    """
    variables: Dict[str, Any] = {
        'projectName': group,
        'tagsData': json.dumps(tags)
    }
    data: Dict[str, Any] = {
        'query': query,
        'variables': variables
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
