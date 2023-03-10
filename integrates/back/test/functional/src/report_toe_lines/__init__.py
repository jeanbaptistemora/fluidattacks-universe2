# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)


async def put_mutation(
    *,
    user: str,
    group_name: str,
    verification_code: str,
) -> dict:
    query: str = """
        query RequestGroupToeLines(
            $groupName: String!,
            $verificationCode: String!
        ) {
            toeLinesReport(
                groupName: $groupName
                verificationCode: $verificationCode
            ) {
                success
            }
        }
    """
    data: dict = {
        "query": query,
        "variables": {
            "groupName": group_name,
            "verificationCode": verification_code,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
