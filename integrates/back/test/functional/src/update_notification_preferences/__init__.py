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
from decimal import (
    Decimal,
)


async def get_result_mutation(
    *,
    user: str,
    severity: Decimal,
    mail: list[str],
    sms: list[str],
) -> dict:
    mutation: str = """
        mutation UpdateNotificationsPreferences(
            $email: [NotificationsName!]!
            $severity: Float!
            $sms: [NotificationsName]
        ) {
            updateNotificationsPreferences(
                notificationsPreferences: {
                    email: $email
                    parameters: { minSeverity: $severity }
                    sms: $sms
                }
            ) {
                success
            }
        }
    """
    data: dict = {
        "query": mutation,
        "variables": {"email": mail, "severity": float(severity), "sms": sms},
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
