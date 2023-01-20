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
    finding_id: str,
) -> dict:
    query: str = """
        mutation SubmitDraft($findingId: String!) {
            submitDraft(
                findingId: $findingId
            ) {
                success
            }
        }
    """
    data: dict = {"query": query, "variables": {"findingId": finding_id}}

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
