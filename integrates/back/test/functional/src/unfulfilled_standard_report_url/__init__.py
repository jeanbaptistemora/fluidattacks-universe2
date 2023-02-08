# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Optional,
)


async def get_result(
    *,
    user: str,
    group_name: str,
    unfulfilled_standards: Optional[list[str]] = None,
) -> dict[str, Any]:
    query: str = """
        query RequestGroupReport(
            $groupName: String!
            $verificationCode: String!
            $unfulfilledStandards: [String!]
        ) {
            unfulfilledStandardReportUrl(
            groupName: $groupName
            verificationCode: $verificationCode
            unfulfilledStandards: $unfulfilledStandards
            )
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "groupName": group_name,
            "verificationCode": "123",
        },
    }
    if unfulfilled_standards is not None:
        data["variables"]["unfulfilledStandards"] = unfulfilled_standards
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
