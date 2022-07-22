# pylint: disable=invalid-name
"""
Remove daily digest notification preference from stakeholders
https://gitlab.com/fluidattacks/universe/-/issues/6861

Execution Time:    2022-07-22 at 19:33:08 UTC
Finalization Time: 2022-07-22 at 19:34:19 UTC
"""


from aioextensions import (
    collect,
    run,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
    StakeholderMetadataToUpdate,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_user(user: Stakeholder, progress: float) -> None:
    if "DAILY_DIGEST" in user.notifications_preferences.email:
        new_preferences = [
            item
            for item in user.notifications_preferences.email
            if item != "DAILY_DIGEST"
        ]
        await stakeholders_model.update_metadata(
            email=user.email,
            metadata=StakeholderMetadataToUpdate(
                notifications_preferences=NotificationsPreferences(
                    email=new_preferences
                )
            ),
        )
        LOGGER_CONSOLE.info(
            "User processed",
            extra={
                "extra": {
                    "user email": user.email,
                    "progress": round(progress, 2),
                }
            },
        )


async def main() -> None:
    all_stakeholders = await stakeholders_model.get_all_stakeholders()
    LOGGER_CONSOLE.info(
        "Active users",
        extra={"extra": {"users_len": len(all_stakeholders)}},
    )
    await collect(
        tuple(
            process_user(
                user=stakeholder, progress=count / len(all_stakeholders)
            )
            for count, stakeholder in enumerate(all_stakeholders)
        ),
        workers=16,
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
