# type: ignore

# pylint: disable=import-error,invalid-name
"""
Populate the enrollment items for the old stakeholders

Execution Time:    2022-08-04 at 20:14:17 UTC
Finalization Time: 2022-08-04 at 20:16:08 UTC
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
from db_model.organizations.types import (
    Organization,
)
from db_model.roots.types import (
    Root,
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
from organizations import (
    domain as orgs_domain,
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
    stakeholder_groups = await loaders.group.load_many(stakeholder_group_names)
    return groups_utils.filter_active_groups(tuple(stakeholder_groups))


async def get_stakeholder_organizations(
    loaders: Dataloaders,
    stakeholder: Stakeholder,
    org_ids: set,
) -> tuple[Organization, ...]:
    stakeholder_orgs = await loaders.stakeholder_organizations_access.load(
        stakeholder.email
    )
    organization_ids: list[str] = [
        org.organization_id
        for org in stakeholder_orgs
        if org.organization_id in org_ids
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
    loaders: Dataloaders,
    stakeholder: Stakeholder,
    org_ids: set,
    progress: float,
) -> None:
    stakeholder_organizations = await get_stakeholder_organizations(
        loaders=loaders, stakeholder=stakeholder, org_ids=org_ids
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
    stakeholder_roots: tuple[Root, ...] = tuple(
        chain.from_iterable(
            await loaders.group_roots.load_many(
                list({group.name for group in stakeholder_groups})
            )
        )
    )
    if stakeholder_roots and not await enrollment_exists(loaders, stakeholder):
        print(stakeholder.email)
        await enrollment_model.add(
            enrollment=Enrollment(
                email=stakeholder.email,
                enrolled=True,
                trial=Trial(
                    completed=True,
                    extension_date=datetime_utils.get_utc_now(),
                    extension_days=0,
                    start_date=datetime_utils.get_utc_now(),
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
    org_ids = set()
    async for org_id, _, _ in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        org_ids.add(org_id)
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
                org_ids=org_ids,
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
