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

USERS_TABLE = "FI_users"


async def main() -> None:
    users = await operations_legacy.scan(USERS_TABLE, {})
    for user in users:
        await users_model.update_user(
            user_email=user["email"],
            notifications_preferences={"email": ["VULNERABILITY_ASSIGNED"]},
        )


if __name__ == "__main__":
    run(main())
