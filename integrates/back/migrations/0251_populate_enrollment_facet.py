# pylint: disable=invalid-name
"""
Populate the enrollment items for the old stakeholders
"""
from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    EnrollmentNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    enrollment as enrollment_model,
    stakeholders as stakeholders_model,
)
from db_model.enrollment.types import (
    Enrollment,
    Trial,
)
from db_model.groups.types import (
    Group,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
    organizations as orgs_utils,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def get_organization_groups_by_stakeholder(
    loaders: Dataloaders, stakeholder: Stakeholder, organization: Organization
) -> tuple[Group, ...]:
    stakeholder_group_names: list[
        str
    ] = await groups_domain.get_groups_by_stakeholder(
        loaders, stakeholder.email, organization_id=organization.id
    )
    stakeholder_groups: tuple[Group, ...] = await loaders.group.load_many(
        stakeholder_group_names
    )
    return groups_utils.filter_active_groups(stakeholder_groups)


async def get_stakeholder_organizations(
    loaders: Dataloaders, stakeholder: Stakeholder
) -> tuple[Organization, ...]:
    stakeholder_orgs: tuple[
        OrganizationAccess, ...
    ] = await loaders.stakeholder_organizations_access.load(stakeholder.email)
    organization_ids: list[str] = [
        org.organization_id for org in stakeholder_orgs
    ]
    organizations = await loaders.organization.load_many(organization_ids)
    return orgs_utils.filter_active_organizations(organizations)


async def enrollment_exists(
    loaders: Dataloaders,
    stakeholder: Stakeholder,
) -> bool:
    try:
        enrollment: Enrollment = await loaders.enrollment.load(
            stakeholder.email
        )
        return enrollment.enrolled
    except EnrollmentNotFound:
        return False


async def process_stakeholder(
    loaders: Dataloaders, stakeholder: Stakeholder, progress: float
) -> None:
    stakeholder_organizations = await get_stakeholder_organizations(
        loaders=loaders, stakeholder=stakeholder
    )
    stakeholder_groups = tuple(
        chain.from_iterable(
            await collect(
                get_organization_groups_by_stakeholder(
                    loaders=loaders,
                    stakeholder=stakeholder,
                    organization=organization,
                )
                for organization in stakeholder_organizations
            )
        )
    )
    if stakeholder_groups and not await enrollment_exists(
        loaders, stakeholder
    ):
        await enrollment_model.add(
            enrollment=Enrollment(
                email=stakeholder.email,
                enrolled=True,
                trial=Trial(
                    completed=True,
                    extension_date=datetime_utils.get_iso_date(),
                    extension_days=0,
                    start_date=datetime_utils.get_iso_date(),
                ),
            )
        )

    LOGGER_CONSOLE.info(
        "stakeholder processed",
        extra={
            "extra": {
                "stakeholder email": stakeholder.email,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_stakeholders = await stakeholders_model.get_all_stakeholders()
    LOGGER_CONSOLE.info(
        "All stakeholders",
        extra={"extra": {"stakeholders_len": len(all_stakeholders)}},
    )
    await collect(
        tuple(
            process_stakeholder(
                loaders=loaders,
                stakeholder=stakeholder,
                progress=count / len(all_stakeholders),
            )
            for count, stakeholder in enumerate(all_stakeholders)
        ),
        workers=100,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
