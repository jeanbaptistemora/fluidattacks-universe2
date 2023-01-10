from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.types import (
    PoliciesToUpdate,
)
from freezegun import (
    freeze_time,
)
from organizations import (
    domain as orgs_domain,
)
import pytest
from schedulers import (
    remove_inactive_stakeholders,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
@freeze_time("2021-01-01")
async def test_remove_inactive_stakeholders() -> None:
    org_name = "imamura"
    loaders: Dataloaders = get_new_context()
    organization: Organization = await loaders.organization.load(org_name)
    org_id = organization.id
    org_stakeholders: tuple[
        Stakeholder, ...
    ] = await orgs_domain.get_stakeholders(loaders, org_id)
    org_stakeholders_emails = [
        stakeholder.email for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == [
        "inactive_imamura1@fluidattacks.com",  # NOSONAR
        "inactive_imamura2@fluidattacks.com",  # NOSONAR
    ]
    inactive_stakeholder1 = await loaders.stakeholder.load(
        "inactive_imamura1@fluidattacks.com"
    )
    assert inactive_stakeholder1
    inactive_stakeholder2 = await loaders.stakeholder.load(
        "inactive_imamura2@fluidattacks.com"
    )
    assert inactive_stakeholder2

    await remove_inactive_stakeholders.main()

    loaders = get_new_context()
    org_stakeholders = await orgs_domain.get_stakeholders(loaders, org_id)
    org_stakeholders_emails = [
        stakeholder.email for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == ["inactive_imamura2@fluidattacks.com"]
    with pytest.raises(StakeholderNotFound):
        await loaders.stakeholder.load("inactive_imamura1@fluidattacks.com")
    inactive_stakeholder2 = await loaders.stakeholder.load(
        "inactive_imamura2@fluidattacks.com"
    )
    assert inactive_stakeholder2

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
    assert not org_stakeholders
    with pytest.raises(StakeholderNotFound):
        await loaders.stakeholder.load("inactive_imamura2@fluidattacks.com")
