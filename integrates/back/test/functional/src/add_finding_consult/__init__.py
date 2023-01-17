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
    content: str,
    finding: str,
    comment_type: str,
    parent_comment: str,
) -> dict:
    mutation: str = """
        mutation AddFindingConsult(
            $content: String!
            $findingId: String!
            $parentComment: GenericScalar!
            $type: FindingConsultType!
        ) {
            addFindingConsult(
                content: $content
                findingId: $findingId
                parentComment: $parentComment
                type: $type
            ) {
                commentId
                success
                __typename
            }
        }
    """
    data: dict = {
        "query": mutation,
        "variables": {
            "content": content,
            "findingId": finding,
            "parentComment": parent_comment,
            "type": comment_type,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
