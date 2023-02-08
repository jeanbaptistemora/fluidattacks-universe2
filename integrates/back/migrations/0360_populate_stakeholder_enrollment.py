# pylint: disable=invalid-name
"""
Populates the stakeholder enrolled attribute with data previosly stored
in the enrollment facet

Execution Time:    2023-02-08 at 01:21:07 UTC
Finalization Time: 2023-02-08 at 01:21:55 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.enrollment.types import (
    Enrollment,
)
from db_model.stakeholders import (
    get_all_stakeholders,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from stakeholders import (
    domain as stakeholders_domain,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_user(user: Stakeholder, progress: float) -> None:
    loaders = get_new_context()
    user_email = user.email
    enrollment: Enrollment = await loaders.enrollment.load(user_email)

    await stakeholders_domain.update(
        email=user_email,
        metadata=StakeholderMetadataToUpdate(
            enrolled=enrollment.enrolled,
        ),
    )

    LOGGER_CONSOLE.info(
        "User processed",
        extra={
            "extra": {
                "user email": user.email,
                "enrolled": enrollment.enrolled,
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
