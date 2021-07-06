# pylint: disable=invalid-name
"""
This migration aims to reset the acceptance of the legal notice
for every ASM user as a result of the changes in our legal terms

"""

from aioextensions import (
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
import time
from users import (
    dal as users_dal,
    domain as users_domain,
)

PROD: bool = True


async def main() -> None:
    users = await users_dal.get_all(Attr("legal_remember").eq(True))

    for user in users:
        print(f"Legal terms acceptance of {user['email']} will be reset")

        if PROD:
            await users_domain.update_legal_remember(user["email"], False)
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
