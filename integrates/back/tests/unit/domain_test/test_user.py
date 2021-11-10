from api.mutations.sign_in import (
    autoenroll_user,
)
from context import (
    FI_DEFAULT_ORG,
)
from custom_exceptions import (
    InvalidPushToken,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from organizations.domain import (
    get_id_by_name,
    get_user_organizations,
)
import pytest
from remove_user.domain import (
    remove_user_all_organizations,
)
from subscriptions.domain import (
    get_user_subscriptions,
)
from users import (
    domain as users_domain,
)


@pytest.mark.changes_db
async def test_add_push_token() -> None:
    user_email = "test@mail.com"
    with pytest.raises(InvalidPushToken):
        assert await users_domain.add_push_token(
            user_email, "not-a-push-token"
        )

    valid_token = "ExponentPushToken[something123]"
    assert await users_domain.add_push_token(user_email, valid_token)

    user_attrs = await users_domain.get_attributes(user_email, ["push_tokens"])
    assert "push_tokens" in user_attrs
    assert valid_token in user_attrs["push_tokens"]


@pytest.mark.changes_db
async def test_remove_push_token() -> None:
    user_email = "unittest@fluidattacks.com"
    token = "ExponentPushToken[dummy]"

    attrs_before = await users_domain.get_attributes(
        user_email, ["push_tokens"]
    )
    assert "push_tokens" in attrs_before
    assert token in attrs_before["push_tokens"]

    assert await users_domain.remove_push_token(user_email, token)

    attrs_after = await users_domain.get_attributes(
        user_email, ["push_tokens"]
    )
    assert token not in attrs_after["push_tokens"]


@pytest.mark.asyncio
@pytest.mark.changes_db
async def test_remove_user() -> None:
    organization_id: str = await get_id_by_name(FI_DEFAULT_ORG)
    email: str = "testanewuser@test.test"
    await autoenroll_user(email)
    subscriptions = await get_user_subscriptions(user_email=email)

    assert await users_domain.get_data(email, "email") == email
    assert await get_user_organizations(email) == [organization_id]
    assert len(subscriptions) == 1
    assert subscriptions[0]["sk"]["entity"] == "DIGEST"

    before_remove_authzs = await dynamodb_ops.scan("fi_authz", {})
    before_remove_project_access = await dynamodb_ops.scan(
        "FI_project_access", {}
    )
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
    assert (
        len(
            [
                access
                for access in before_remove_project_access
                if access["user_email"] == email
            ]
        )
        >= 1
    )

    await remove_user_all_organizations(email=email)

    assert await users_domain.get_data(email, "email") == ""
    assert await get_user_organizations(email) == []
    assert await get_user_subscriptions(user_email=email) == []

    after_remove_authzs = await dynamodb_ops.scan("fi_authz", {})
    after_removed_project_access = await dynamodb_ops.scan(
        "FI_project_access", {}
    )
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
    assert (
        len(
            [
                access
                for access in after_removed_project_access
                if access["user_email"] == email
            ]
        )
        == 0
    )
