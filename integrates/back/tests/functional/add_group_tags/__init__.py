# pylint: disable=import-error
from back.tests.functional.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import json
from typing import (
    Any,
    Dict,
    List,
)


async def get_result(
    *,
    user: str,
    group: str,
    tags: List[str],
) -> Dict[str, Any]:
    query: str = """
        mutation AddGroupTagsMutation(
            $groupName: String!,
            $tagsData: JSONString!
        ) {
            addGroupTags(
                tags: $tagsData,
                groupName: $groupName) {
                success
            }
        }
    """
    variables: Dict[str, Any] = {
        "groupName": group,
        "tagsData": json.dumps(tags),
    }
    data: Dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
