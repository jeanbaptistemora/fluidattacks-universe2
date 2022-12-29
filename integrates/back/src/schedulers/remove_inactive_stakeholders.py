from aioextensions import (
    collect,
)
from db_model.stakeholders import (
    get_all_stakeholders,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from newutils import (
    datetime as datetime_utils,
)
from remove_stakeholder.domain import (
    remove_stakeholder_all_organizations,
)
from schedulers.common import (
    info,
)

INACTIVITY_DAYS = 90


async def process_stakeholder(
    modified_by: str,
    stakeholder: Stakeholder,
) -> None:
    if stakeholder.last_login_date is None:
        return

    inactivity_days = (
        datetime_utils.get_utc_now() - stakeholder.last_login_date
    ).days
    if inactivity_days < INACTIVITY_DAYS:
        return

    await remove_stakeholder_all_organizations(
        email=stakeholder.email,
        modified_by=modified_by,
    )
    info(
        "Inactive stakeholder removed",
        extra={
            "email": stakeholder.email,
            "inactivity_days": inactivity_days,
        },
    )


async def remove_inactive_stakeholders() -> None:
    """
    Remove stakeholders for inactivity (no logins) in the defined period.
    """
    modified_by = "integrates@fluidattacks.com"
    all_stakeholders: tuple[Stakeholder, ...] = await get_all_stakeholders()
    info("Stakeholders to process", extra={"item": len(all_stakeholders)})
    await collect(
        tuple(
            process_stakeholder(
                modified_by=modified_by,
                stakeholder=stakeholder,
            )
            for stakeholder in all_stakeholders
        ),
        workers=1,
    )


async def main() -> None:
    await remove_inactive_stakeholders()
