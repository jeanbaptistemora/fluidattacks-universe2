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
