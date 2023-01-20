# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def approve_draft(
    *,
    user: str,
    finding_id: str,
) -> dict:
    query: str = """
        mutation ApproveDraft($draftId: String!) {
            approveDraft(
                draftId: $draftId
            ) {
                success
            }
        }
    """
    data: dict = {"query": query, "variables": {"draftId": finding_id}}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
