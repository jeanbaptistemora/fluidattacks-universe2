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
import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_stakeholder() -> None:
    expected_output = {
        "email": "continuoushacking@gmail.com",
        "role": "user_manager",
        "responsibility": "Test",
        "first_login": "2018-02-28T16:54:12+00:00",
        "last_login": "[186, 33677]",
        "groups": [
            {"name": "asgard"},
            {"name": "barranquilla"},
            {"name": "gotham"},
            {"name": "metropolis"},
            {"name": "monteria"},
            {"name": "oneshottest"},
            {"name": "unittesting"},
        ],
    }
    query = """
        query {
            stakeholder(entity: GROUP,
                    groupName: "unittesting",
                    userEmail: "continuoushacking@gmail.com") {
                email
                role
                responsibility
                firstLogin
                lastLogin
                groups {
                    name
                }
                __typename
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert result["data"]["stakeholder"]["email"] == expected_output.get(
        "email"
    )
    assert result["data"]["stakeholder"]["role"] == expected_output.get("role")
    assert result["data"]["stakeholder"][
        "responsibility"
    ] == expected_output.get("responsibility")
    assert result["data"]["stakeholder"]["firstLogin"] == expected_output.get(
        "first_login"
    )
    assert result["data"]["stakeholder"]["groups"] == expected_output.get(
        "groups"
    )
    assert "stakeholder" in result["data"]
    assert "responsibility" in result["data"]["stakeholder"]


async def test_user_list_groups() -> None:
    query = """
        query {
            listUserGroups(userEmail: "continuoushacking@gmail.com") {
                name
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert result["data"]["listUserGroups"][0]["name"] == "asgard"


@pytest.mark.changes_db
async def test_add_stakeholder() -> None:
    """Check for addStakeholder mutation."""
    query = """
        mutation {
            addStakeholder(
                email: "test@test.com",
                role: USER
            ) {
                success
                email
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session("integratesmanager@gmail.com")
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "addStakeholder" in result["data"]
    assert "success" in result["data"]["addStakeholder"]
    assert "email" in result["data"]["addStakeholder"]


@pytest.mark.changes_db
async def test_grant_stakeholder_access_1() -> None:
    """Check for grantStakeholderAccess mutation."""
    query = """
        mutation {
            grantStakeholderAccess (
            email: "test@test.test"
            groupName: "unittesting"
            responsibility: "test"
            role: USER) {
            success
            grantedStakeholder {
                email
                role
                responsibility
                firstLogin
                lastLogin
            }
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["grantStakeholderAccess"]
    assert "grantedStakeholder" in result["data"]["grantStakeholderAccess"]
    assert (
        "email"
        in result["data"]["grantStakeholderAccess"]["grantedStakeholder"]
    )


@pytest.mark.changes_db
async def test_grant_stakeholder_access_2() -> None:
    """Check for grantStakeholderAccess mutation."""
    query = """
        mutation {
            grantStakeholderAccess (
            email: "test@test.test"
            groupName: "unittesting"
            responsibility: "test"
            role: HACKER) {
                success
                grantedStakeholder {
                    email
                    role
                    responsibility
                    firstLogin
                    lastLogin
                }
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" in result
    assert result["errors"][0]["message"] == (
        "Exception - The previous invitation to this user was requested "
        "less than a minute ago"
    )


@pytest.mark.changes_db
async def test_grant_stakeholder_access_3() -> None:
    """Check for grantStakeholderAccess mutation."""
    query = """
        mutation {
            grantStakeholderAccess (
            email: "test2@test.test"
            groupName: "unittesting"
            responsibility: "test"
            role: HACKER) {
                success
                grantedStakeholder {
                    email
                    role
                    responsibility
                    firstLogin
                    lastLogin
                }
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" in result
    assert result["errors"][0]["message"] == (
        "Exception - Groups with any active Fluid Attacks service can "
        "only have Hackers provided by Fluid Attacks"
    )


@pytest.mark.changes_db
async def test_grant_stakeholder_access_4() -> None:
    """Check for grantStakeholderAccess mutation."""
    query = """
        mutation {
            grantStakeholderAccess (
            email: "test@fluidattacks.com"
            groupName: "unittesting"
            responsibility: "test"
            role: HACKER) {
                success
                grantedStakeholder {
                    email
                    role
                    responsibility
                    firstLogin
                    lastLogin
                }
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["grantStakeholderAccess"]
    assert "grantedStakeholder" in result["data"]["grantStakeholderAccess"]
    assert (
        "email"
        in result["data"]["grantStakeholderAccess"]["grantedStakeholder"]
    )


@pytest.mark.changes_db
async def test_remove_stakeholder_access() -> None:
    """Check for removeStakeholderAccess mutation."""
    query = """
        mutation {
            removeStakeholderAccess (
            groupName: "unittesting"
            userEmail: "test@test.test"
            )
            {
                removedEmail
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["removeStakeholderAccess"]
    assert "removedEmail" in result["data"]["removeStakeholderAccess"]


@pytest.mark.changes_db
async def test_edit_stakeholder() -> None:
    """Check for updateGroupStakeholder mutation."""
    query = """
        mutation {
            updateGroupStakeholder (
            email: "integratesuser2@gmail.com"
            groupName: "unittesting"
            responsibility: "edited"
            role: USER) {
                success
            }
        }
    """
    data = {"query": query}
    request = await create_dummy_session()
    _, result = await graphql(SCHEMA, data, context_value=request)
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupStakeholder"]
