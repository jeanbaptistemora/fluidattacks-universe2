from api.mutations.sign_in import (
    autoenroll_stakeholder,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest
from remove_stakeholder.domain import (
    remove_stakeholder_all_organizations,
)
from subscriptions.domain import (
    get_user_subscriptions,
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_remove_stakeholder() -> None:
    loaders: Dataloaders = get_new_context()
    email: str = "testanewuser@test.test"
    modified_by: str = "admin@test.test"
    await autoenroll_stakeholder(email, "FirstName", "LastName")

    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder.email == email
    assert stakeholder.role == "user"

    await remove_stakeholder_all_organizations(
        loaders=get_new_context(), email=email, modified_by=modified_by
    )
    assert await get_user_subscriptions(user_email=email) == []
