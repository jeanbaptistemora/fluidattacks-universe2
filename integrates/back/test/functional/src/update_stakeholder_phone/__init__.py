# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    new_phone: dict[str, str],
    verification_code: str,
) -> dict[str, Any]:
    query: str = """
    mutation UpdateStakeholderPhoneMutation(
        $newPhone: PhoneInput!
        $verificationCode: String!
    ) {
        updateStakeholderPhone(
            phone: $newPhone
            verificationCode: $verificationCode
        ) {
            success
        }
    }"""
    variables: dict[str, Any] = {
        "newPhone": new_phone,
        "verificationCode": verification_code,
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
