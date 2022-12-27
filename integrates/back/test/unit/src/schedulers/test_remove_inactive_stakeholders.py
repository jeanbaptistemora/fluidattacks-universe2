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
        "deleteimamura@fluidattacks.com",  # NOSONAR
        "nodeleteimamura@fluidattacks.com",  # NOSONAR
    ]
    remove_stakeholder = await loaders.stakeholder.load(
        "deleteimamura@fluidattacks.com"
    )
    remove_stakeholder_exists = bool(remove_stakeholder)
    assert remove_stakeholder_exists
    noremove_stakeholder = await loaders.stakeholder.load(
        "nodeleteimamura@fluidattacks.com"
    )
    noremove_stakeholder_exists = bool(noremove_stakeholder)
    assert noremove_stakeholder_exists

    await remove_inactive_stakeholders.main()

    loaders = get_new_context()
    org_stakeholders = await orgs_domain.get_stakeholders(loaders, org_id)
    org_stakeholders_emails = [
        stakeholder.email for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == ["nodeleteimamura@fluidattacks.com"]
    with pytest.raises(StakeholderNotFound):
        await loaders.stakeholder.load("deleteimamura@fluidattacks.com")
    noremove_stakeholder = await loaders.stakeholder.load(
        "nodeleteimamura@fluidattacks.com"
    )
    noremove_stakeholder_exists = bool(noremove_stakeholder)
    assert noremove_stakeholder_exists
