# pylint: disable=invalid-name
"""
Update notifications preferences to users

Execution Time: 2022-03-01 at 14:00:24 UTC
Finalization Time: 2022-03-01 at 14:01:42 UTC

Update preferences

Execution Time: 2022-03-02 at 20:55:04 UTC
Finalization Time: 2022-03-02 at 20:56:26 UTC

Removed preferences

Execution Time: 2022-03-03 at 15:33:06 UTC
Finalization Time: 2022-03-03 at 15:34:31 UTC

Added Vulnerability report

Execution Time: 2022-03-18 at 14:26:17 UTC
Finalization Time: 2022-03-18 at 14:27:50 UTC

Added Event report

Execution Time: 2022-03-25 at 14:27:37 UTC
Finalization Time: 2022-03-25 at 14:29:05 UTC

Added Reminder Notification

Execution Time: 2022-04-18 at 19:22:42 UTC
Finalization Time: 2022-04-18 at 19:24:20 UTC

Added notifications preferences

Execution Time: 2022-05-13 at 16:57:29 UTC
Finalization Time: 2022-05-13 at 17:04:16 UTC
"""


from aioextensions import (
    run,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from dynamodb import (
    operations_legacy,
)
import time

USERS_TABLE = "FI_users"


async def main() -> None:
    users = await operations_legacy.scan(USERS_TABLE, {})
    for user in users:
        await stakeholders_model.update_metadata(
            stakeholder_email=user["email"],
            notifications_preferences={
                "email": [
                    "ACCESS_GRANTED",
                    "AGENT_TOKEN",
                    "CHARTS_REPORT",
                    "DAILY_DIGEST",
                    "EVENT_REPORT",
                    "FILE_UPDATE",
                    "GROUP_INFORMATION",
                    "GROUP_REPORT",
                    "NEW_COMMENT",
                    "NEW_DRAFT",
                    "PORTFOLIO_UPDATE",
                    "REMEDIATE_FINDING",
                    "REMINDER_NOTIFICATION",
                    "ROOT_UPDATE",
                    "SERVICE_UPDATE",
                    "UNSUBSCRIPTION_ALERT",
                    "UPDATED_TREATMENT",
                    "VULNERABILITY_ASSIGNED",
                    "VULNERABILITY_REPORT",
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
