from api.mutations.sign_in import (
    autoenroll_stakeholder,
)
from custom_exceptions import (
    InvalidPushToken,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import pytest
from remove_stakeholder.domain import (
    remove_stakeholder_all_organizations,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from subscriptions.domain import (
    get_user_subscriptions,
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add_push_token() -> None:
    loaders: Dataloaders = get_new_context()
    user_email = "test@mail.com"
    with pytest.raises(InvalidPushToken):
        assert await stakeholders_domain.add_push_token(
            loaders, user_email, "not-a-push-token"
        )

    valid_token = "ExponentPushToken[something123]"
    assert await stakeholders_domain.add_push_token(
        loaders, user_email, valid_token
    )

    user_attrs: Stakeholder = await loaders.stakeholder.load(user_email)
    assert valid_token in user_attrs.push_tokens


@pytest.mark.changes_db
async def test_remove_stakeholder() -> None:
    email: str = "testanewuser@test.test"
    modified_by: str = "admin@test.test"
    await autoenroll_stakeholder(email)
    subscriptions = await get_user_subscriptions(user_email=email)

    assert await stakeholders_domain.get_data(email, "email") == email
    assert len(subscriptions) == 1
    assert subscriptions[0]["sk"]["entity"] == "DIGEST"

    before_remove_authzs = await dynamodb_ops.scan("fi_authz", {})
    assert (
        len(
            [
                authz
                for authz in before_remove_authzs
                if authz["subject"] == email
            ]
        )
        >= 1
    )

    await remove_stakeholder_all_organizations(
        loaders=get_new_context(), email=email, modified_by=modified_by
    )

    assert await stakeholders_domain.get_data(email, "email") == {}
    assert await get_user_subscriptions(user_email=email) == []

    after_remove_authzs = await dynamodb_ops.scan("fi_authz", {})
    assert (
        len(
            [
                authz
                for authz in after_remove_authzs
                if authz["subject"] == email
            ]
        )
        == 0
    )
