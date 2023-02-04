from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.types import (
    PoliciesToUpdate,
)
from freezegun import (
    freeze_time,
)
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
import pytest
from schedulers import (
    remove_inactive_stakeholders,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
@freeze_time("2021-01-01T00:00:00+00:00")
async def test_remove_inactive_stakeholders() -> None:
    org_name = "imamura"
    loaders: Dataloaders = get_new_context()
    organization = await orgs_utils.get_organization(loaders, org_name)
    org_id = organization.id
    org_stakeholders = await orgs_domain.get_stakeholders(loaders, org_id)
    org_stakeholders_emails = [
        stakeholder.email for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == [
        "active_imamura3@fluidattacks.com",  # NOSONAR
        "inactive_imamura1@fluidattacks.com",  # NOSONAR
        "inactive_imamura2@fluidattacks.com",  # NOSONAR
    ]
    active_stakeholder3 = await loaders.stakeholder.load(
        "active_imamura3@fluidattacks.com"
    )
    assert active_stakeholder3
    inactive_stakeholder1 = await loaders.stakeholder.load(
        "inactive_imamura1@fluidattacks.com"
    )
    assert inactive_stakeholder1
    inactive_stakeholder2 = await loaders.stakeholder.load(
        "inactive_imamura2@fluidattacks.com"
    )
    assert inactive_stakeholder2

    # First run, default inactivity period policy
    await remove_inactive_stakeholders.main()
    loaders = get_new_context()
    org_stakeholders = await orgs_domain.get_stakeholders(loaders, org_id)
    org_stakeholders_emails = [
        stakeholder.email for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == [
        "active_imamura3@fluidattacks.com",
        "inactive_imamura2@fluidattacks.com",
    ]
    active_stakeholder3 = await loaders.stakeholder.load(
        "active_imamura3@fluidattacks.com"
    )
    assert active_stakeholder3
    inactive_stakeholder2 = await loaders.stakeholder.load(
        "inactive_imamura2@fluidattacks.com"
    )
    assert inactive_stakeholder2
    with pytest.raises(StakeholderNotFound):
        await loaders.stakeholder.load("inactive_imamura1@fluidattacks.com")

    # Second run, set inactivity period policy
    await orgs_domain.update_policies(
        loaders=get_new_context(),
        organization_id=org_id,
        organization_name=org_name,
        user_email="integrates@fluidattacks.com",
        policies_to_update=PoliciesToUpdate(
            inactivity_period=89,
        ),
    )
    await remove_inactive_stakeholders.main()
    loaders = get_new_context()
    org_stakeholders = await orgs_domain.get_stakeholders(loaders, org_id)
    org_stakeholders_emails = [
        stakeholder.email for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == [
        "active_imamura3@fluidattacks.com",
    ]
    active_stakeholder3 = await loaders.stakeholder.load(
        "active_imamura3@fluidattacks.com"
    )
    assert active_stakeholder3
    with pytest.raises(StakeholderNotFound):
        await loaders.stakeholder.load("inactive_imamura2@fluidattacks.com")
