from back.tests.functional.group_manager.utils import (
    get_result,
)
from custom_exceptions import (
    UserNotInOrganization,
)
from dataloaders import (
    get_new_context,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("old")
async def test_organization() -> None:  # pylint: disable=too-many-statements
    context = get_new_context()
    org_name = "OKADA"
    group_name = "unittesting"
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    stakeholder = "org_testuser_3@gmail.com"
    stakeholder_role = "CUSTOMER"
    query = f"""
        mutation {{
            grantStakeholderOrganizationAccess(
                organizationId: "{org_id}",
                phoneNumber: "-",
                role: {stakeholder_role},
                userEmail: "{stakeholder}"
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
    assert "errors" not in result
    assert result["data"]["grantStakeholderOrganizationAccess"]["success"]
    assert (
        result["data"]["grantStakeholderOrganizationAccess"][
            "grantedStakeholder"
        ]["email"]
        == stakeholder
    )
    result = await get_result(data, stakeholder=stakeholder)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
    result = await get_result(data, stakeholder="madeupuser@gmail.com")
    exe = UserNotInOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]

    context = get_new_context()
    phone_number = "9999999999"
    query = f"""
        mutation {{
            editStakeholderOrganization(
                organizationId: "{org_id}",
                phoneNumber: "{phone_number}",
                role: {stakeholder_role},
                userEmail: "{stakeholder}"
            ) {{
                success
                modifiedStakeholder {{
                    email
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["editStakeholderOrganization"]["success"]
    assert (
        result["data"]["editStakeholderOrganization"]["modifiedStakeholder"][
            "email"
        ]
        == stakeholder
    )

    context = get_new_context()
    query = f"""
        query {{
            stakeholder(entity: ORGANIZATION,
                    organizationId: "{org_id}",
                    userEmail: "{stakeholder}") {{
                email
                groups{{
                    name
                }}
                phoneNumber
                role
                __typename
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["stakeholder"]["phoneNumber"] == phone_number

    context = get_new_context()
    query = f"""
        mutation {{
            updateOrganizationPolicies(
                maxAcceptanceDays: 5,
                maxAcceptanceSeverity: 8.5,
                maxNumberAcceptations: 3,
                minAcceptanceSeverity: 1.5,
                organizationId: "{org_id}",
                organizationName: "{org_name}"
            ) {{
                success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    exe = UserNotInOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]

    context = get_new_context()
    query = f"""
        query {{
            organization(organizationId: "{org_id}") {{
                id
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptations
                minAcceptanceSeverity
                name
                groups {{
                    name
                }}
                stakeholders {{
                    email
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    groups = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["maxAcceptanceDays"] == 60
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 10.0
    assert result["data"]["organization"]["maxNumberAcceptations"] == 2
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 0.0
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert group_name in groups
    assert "continuoushack2@gmail.com" in stakeholders
    exe = UserNotInOrganization()
    result = await get_result(data, stakeholder="madeupuser@gmail.com")
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]

    context = get_new_context()
    query = f"""
        mutation {{
            removeStakeholderOrganizationAccess(
                organizationId: "{org_id}",
                userEmail: "{stakeholder}"
            ) {{
                success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["removeStakeholderOrganizationAccess"]["success"]

    context = get_new_context()
    query = f"""
        query {{
            organization(organizationId: "{org_id}") {{
                stakeholders {{
                    email
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    stakeholders = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert stakeholder not in stakeholders
