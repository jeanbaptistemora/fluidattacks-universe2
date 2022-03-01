# pylint: disable=invalid-name
from aioextensions import (
    run,
)
from db_model import (
    users as users_model,
)
from dynamodb import (
    operations_legacy,
)
import time

USERS_TABLE = "FI_users"


async def main() -> None:
    users = await operations_legacy.scan(USERS_TABLE, {})
    for user in users:
        await users_model.update_user(
            user_email=user["email"],
            notifications_preferences={"email": ["VULNERABILITY_ASSIGNED"]},
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
