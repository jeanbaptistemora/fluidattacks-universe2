# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration aims to reset the acceptance of the legal notice
for every ASM user as a result of the changes in our legal terms

Execution Time:    2021-07-06 at 18:23:57 UTC-05
Finalization Time: 2021-07-06 at 18:35:28 UTC-05
"""

from aioextensions import (
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from stakeholders import (
    dal as stakeholders_dal,
    domain as stakeholders_domain,
)
import time

PROD: bool = True


async def main() -> None:
    users = await stakeholders_dal.get_all(Attr("legal_remember").eq(True))

    for user in users:
        print(f"Legal terms acceptance of {user['email']} will be reset")

        if PROD:
            await stakeholders_domain.update_legal_remember(
                user["email"], False
            )
            print(f"Legal terms acceptance of {user['email']} has been reset")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
