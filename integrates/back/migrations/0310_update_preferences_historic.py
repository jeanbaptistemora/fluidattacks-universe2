# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name
"""
update notification preferences field to historic state

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from db_model.stakeholders import (
    get_all_stakeholders,
    update_state,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderState,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_user(user: Stakeholder, progress: float) -> None:
    if user.state.modified_date != "":
        return

    await update_state(
        user_email=user.email,
        state=StakeholderState(
            modified_by=user.email,
            modified_date=datetime_utils.get_iso_date(),
            notifications_preferences=user.notifications_preferences,
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
    all_stakeholders = await get_all_stakeholders()
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
