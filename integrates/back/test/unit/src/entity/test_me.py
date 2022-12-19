# pylint: disable=import-error
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.test.unit.src.utils import (
    create_dummy_session,
)
from dataloaders import (
    apply_context_attrs,
)
import pytest

pytestmark = pytest.mark.asyncio


async def test_me() -> None:
    """Check Me query"""
    query = """{
        me(callerOrigin: "API") {
            accessToken
            company {
                domain
                trial {
                    completed
                }
            }
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
    request = apply_context_attrs(request)  # type: ignore
    _, result = await graphql(SCHEMA, data, context_value=request)
    expected_groups = ["unittesting", "oneshottest"]
    assert "me" in result["data"]
    assert "role" in result["data"]["me"]
    assert result["data"]["me"]["role"] == "user"
    assert sorted(result["data"]["me"]["permissions"]) == [
        "api_mutations_add_organization_mutate",
        "api_mutations_update_stakeholder_phone_mutate",
        "api_mutations_verify_stakeholder_mutate",
    ]
    assert result["data"]["me"]["callerOrigin"] == "API"
    assert "tags" in result["data"]["me"]
    for tag in result["data"]["me"]["tags"]:
        assert "name" in tag
        assert "groups" in tag
        if tag["name"] == "test-groups":
            output = [proj["name"] for proj in tag["groups"]]
            assert sorted(output) == sorted(expected_groups)
    assert result["data"]["me"]["company"] == {
        "domain": "gmail.com",
        "trial": {"completed": True},
    }
