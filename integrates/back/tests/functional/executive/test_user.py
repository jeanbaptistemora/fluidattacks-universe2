# Standard libraries
import pytest

# Local libraries
from back.tests.functional.executive.utils import get_result
from dataloaders import get_new_context


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("old")
async def test_user():
    context = get_new_context()
    group_name = "unittesting"
    stakeholder = "stakeholder@fluidattacks.com"
    phone_number = "3453453453"
    responsibility = "test"
    role = "EXECUTIVE"
    query = f"""
        mutation {{
            grantStakeholderAccess (
                email: "{stakeholder}",
                phoneNumber: "{phone_number}"
                projectName: "{group_name}",
                responsibility: "{responsibility}",
                role: {role}
            ) {{
            success
                grantedStakeholder {{
                    email
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    context = get_new_context()
    query = f"""
        query {{
            stakeholder(entity: PROJECT,
                    projectName: "{group_name}",
                    userEmail: "{stakeholder}") {{
                email
                role
                responsibility
                phoneNumber
                firstLogin
                lastLogin
                projects {{
                    name
                }}
                __typename
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    context = get_new_context()
    phone_number = "17364735"
    responsibility = "edited"
    role = "GROUP_MANAGER"
    query = f"""
        mutation {{
            editStakeholder (
                email: "{stakeholder}",
                phoneNumber: "{phone_number}",
                projectName: "{group_name}"
                responsibility: "{responsibility}",
                role: {role}
            ) {{
                success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    context = get_new_context()
    query = f"""
        mutation {{
            removeStakeholderAccess (
                projectName: "{group_name}",
                userEmail: "{stakeholder}"
            )
            {{
                removedEmail
                success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
