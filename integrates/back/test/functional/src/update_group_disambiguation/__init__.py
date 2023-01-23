# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def get_result(
    *,
    user: str,
    group: str,
    disambiguation: str,
) -> dict:
    query: str = """
        mutation UpdateGroupDisambiguation(
            $disambiguation: String
            $groupName: String!
        ) {
            updateGroupDisambiguation(
                disambiguation: $disambiguation
                groupName: $groupName
            ) {
                success
            }
        }
    """
    data: dict = {
        "query": query,
        "variables": {"groupName": group, "disambiguation": disambiguation},
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
