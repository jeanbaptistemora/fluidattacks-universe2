# pylint: disable=invalid-name
"""
Update notifications preferences to users

Execution Time: 2022-03-01 at 14:00:24 UTC
Finalization Time: 2022-03-01 at 14:01:42 UTC
"""


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
            notifications_preferences={
                "email": [
                    "ACCESS_GRANTED",
                    "CHARTS_REPORT",
                    "DAILY_DIGEST",
                    "DELETE_FINDING",
                    "FILE_REMOVED",
                    "FILE_UPLOADED",
                    "GROUP_REPORT",
                    "NEW_COMMENT",
                    "NEW_DRAFT",
                    "NEW_REMEDIATED",
                    "REMEDIATE_FINDING",
                    "ROOT_DEACTIVATED",
                    "ROOT_MOVED",
                    "UNSUBMITTED_DRAFT",
                    "UPDATED_TREATMENT",
                    "VULNERABILITY_ASSIGNED",
                ]
            },
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
