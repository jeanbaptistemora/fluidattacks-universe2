from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from dataloaders import (
    apply_context_attrs,
)
from datetime import (
    datetime,
    timedelta,
)
import pytest

pytestmark = pytest.mark.asyncio


async def test_me() -> None:
    """Check Me query"""
    query = """{
        me(callerOrigin: "API") {
            accessToken
            tags(organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3") {
                name
                groups {
                    name
                }
            }
            remember
            role
            permissions
            callerOrigin
            __typename
        }
    }"""
    data = {"query": query}
    user_email = "integratesuser@gmail.com"
    request = await create_dummy_session(user_email)
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)
    expected_groups = ["unittesting", "oneshottest"]
    assert "me" in result["data"]
    assert "role" in result["data"]["me"]
    assert result["data"]["me"]["role"] == "customeradmin"
    assert result["data"]["me"]["permissions"] == []
    assert result["data"]["me"]["callerOrigin"] == "API"
    assert "tags" in result["data"]["me"]
    for tag in result["data"]["me"]["tags"]:
        assert "name" in tag
        assert "groups" in tag
        if tag["name"] == "test-projects":
            output = [proj["name"] for proj in tag["groups"]]
            assert sorted(output) == sorted(expected_groups)


@pytest.mark.changes_db
async def test_sign_in() -> None:
    """Check for signIn mutation."""
    query = """
        mutation {
            signIn(
                authToken: "badtoken",
                provider: GOOGLE
            ) {
                sessionJwt
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert not result["data"]["signIn"]["success"]


@pytest.mark.changes_db
async def test_update_access_token() -> None:
    """Check for updateAccessToken mutation."""
    query = """
        mutation updateAccessToken ($expirationTime: Int!) {
            updateAccessToken(expirationTime: $expirationTime) {
                sessionJwt
                success
            }
        }
    """
    expiration_time = datetime.utcnow() + timedelta(weeks=8)
    int_expiration_time = int(expiration_time.timestamp())

    data = {
        "query": query,
        "variables": {"expirationTime": int_expiration_time},
    }
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "updateAccessToken" in result["data"]
    assert "success" in result["data"]["updateAccessToken"]


@pytest.mark.changes_db
async def test_invalidate_access_token() -> None:
    """Check invalidateAccessToken query"""
    query = """
        mutation {
            invalidateAccessToken {
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "invalidateAccessToken" in result["data"]
    assert "success" in result["data"]["invalidateAccessToken"]


@pytest.mark.changes_db
async def test_accept_legal() -> None:
    """Check acceptLegal query"""
    query = """
        mutation {
            acceptLegal(remember: true) {
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "acceptLegal" in result["data"]
    assert "success" in result["data"]["acceptLegal"]


@pytest.mark.changes_db
async def test_add_push_token() -> None:
    """Check add_push_token mutation"""
    query = """
        mutation {
            addPushToken(token: "ExponentPushToken[something123]") {
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "error" not in result
    assert result["data"]["addPushToken"]["success"]
