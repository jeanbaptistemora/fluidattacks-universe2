# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    new_phone: Dict[str, str],
    verification_code: str,
) -> Dict[str, Any]:
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
    variables: Dict[str, Any] = {
        "newPhone": new_phone,
        "verificationCode": verification_code,
    }
    data: Dict[str, Any] = {"query": query, "variables": variables}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
