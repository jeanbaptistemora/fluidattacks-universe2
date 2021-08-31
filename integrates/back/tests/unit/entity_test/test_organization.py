from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from context import (
    FI_DEFAULT_ORG,
)
from custom_exceptions import (
    InvalidOrganization,
    UserNotInOrganization,
)
from dataloaders import (
    apply_context_attrs,
)
from decimal import (
    Decimal,
)
from organizations import (
    domain as orgs_domain,
)
import pytest
from string import (
    Template,
)
from typing import (
    Any,
    Dict,
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


async def _get_result_async(
    data: Dict[str, Any], stakeholder: str = "integratesmanager@gmail.com"
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username=stakeholder)
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


@pytest.mark.changes_db
async def test_add_organization() -> None:
    mutation_tpl = Template(
        """
        mutation {
            addOrganization(name: "$name") {
                organization {
                    id
                    name
                }
                success
            }
        }
    """
    )

    name = "AKAME"
    data = {"query": mutation_tpl.substitute(name=name)}
    result = await _get_result_async(data)

    assert "errors" not in result
    assert result["data"]["addOrganization"]["success"]
    assert (
        result["data"]["addOrganization"]["organization"]["name"]
        == name.lower()
    )
    assert result["data"]["addOrganization"]["organization"]["id"].startswith(
        "ORG"
    )

    name = "MADEUP-NAME"
    data = {"query": mutation_tpl.substitute(name=name)}
    exe = InvalidOrganization()
    result = await _get_result_async(data)
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]


@pytest.mark.changes_db
async def test_update_organization_stakeholder() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    stakeholder = "org_testgroupmanager1@gmail.com"
    query = Template(
        """
        mutation {
            updateOrganizationStakeholder(
                organizationId: "$org_id",
                phoneNumber: "-",
                role: $role,
                userEmail: "$email"
            ) {
                success
                modifiedStakeholder {
                    email
                }
            }
        }
    """
    )

    data = {
        "query": query.substitute(
            org_id=org_id, role="CUSTOMER", email=stakeholder
        )
    }
    result = await _get_result_async(data)
    assert "errors" not in result
    assert result["data"]["updateOrganizationStakeholder"]["success"]
    assert (
        result["data"]["updateOrganizationStakeholder"]["modifiedStakeholder"][
            "email"
        ]
        == stakeholder
    )

    data = {
        "query": query.substitute(
            org_id=org_id, role="CUSTOMERADMIN", email=stakeholder
        )
    }
    result = await _get_result_async(data, stakeholder=stakeholder)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    data = {
        "query": query.substitute(
            org_id=org_id, role="CUSTOMERADMIN", email="madeupuser@gmail.com"
        )
    }
    result = await _get_result_async(data)
    exe = UserNotInOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]


@pytest.mark.changes_db
async def test_grant_stakeholder_organization_access() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    stakeholder = "org_testuser6@gmail.com"
    query = Template(
        """
        mutation {
            grantStakeholderOrganizationAccess(
                organizationId: "$org_id",
                phoneNumber: "-",
                role: $role,
                userEmail: "$email"
            ) {
                success
                grantedStakeholder {
                    email
                }
            }
        }
    """
    )

    data = {
        "query": query.substitute(
            email=stakeholder, org_id=org_id, role="CUSTOMER"
        )
    }
    result = await _get_result_async(data)
    assert "errors" not in result
    assert result["data"]["grantStakeholderOrganizationAccess"]["success"]
    assert (
        result["data"]["grantStakeholderOrganizationAccess"][
            "grantedStakeholder"
        ]["email"]
        == stakeholder
    )

    default_org_id: str = await orgs_domain.get_id_by_name(FI_DEFAULT_ORG)
    assert await orgs_domain.has_user_access(org_id, stakeholder)
    assert not await orgs_domain.has_user_access(default_org_id, stakeholder)

    data = {
        "query": query.substitute(
            email="org_testuser7@gmail.com",
            org_id=default_org_id,
            role="CUSTOMER",
        )
    }
    result = await _get_result_async(data)
    assert "errors" not in result
    assert result["data"]["grantStakeholderOrganizationAccess"]["success"]
    assert await orgs_domain.has_user_access(
        default_org_id, "org_testuser7@gmail.com"
    )

    data = {
        "query": query.substitute(
            email="madeupuser@gmail.com", org_id=org_id, role="CUSTOMER"
        )
    }
    result = await _get_result_async(data, stakeholder=stakeholder)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    data = {
        "query": query.substitute(
            email="madeupuser@gmail.com", org_id=org_id, role="CUSTOMER"
        )
    }
    result = await _get_result_async(data, "madeupuser@gmail.com")
    exe = UserNotInOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]


@pytest.mark.changes_db
async def test_remove_stakeholder_organization_access() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    stakeholder = "org_testuser4@gmail.com"
    query = Template(
        f"""
        mutation {{
            removeStakeholderOrganizationAccess(
                organizationId: "{org_id}",
                userEmail: "$email"
            ) {{
                success
            }}
        }}
    """
    )

    data = {"query": query.substitute(email=stakeholder)}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert result["data"]["removeStakeholderOrganizationAccess"]["success"]

    data = {"query": query.substitute(email="org_testuser2@gmail.com")}
    result = await _get_result_async(data, stakeholder="madeupuser@gmail.com")
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    data = {"query": query.substitute(email="madeupuser@gmail.com")}
    result = await _get_result_async(data)
    exe = UserNotInOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]


@pytest.mark.changes_db
async def test_update_organization_policies() -> None:
    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"
    org_name = "hajime"
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
    result = await _get_result_async(data)
    assert "errors" not in result
    assert result["data"]["updateOrganizationPolicies"]["success"]

    result = await _get_result_async(
        data, stakeholder="org_testuser5@gmail.com"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    result = await _get_result_async(data, stakeholder="madeupuser@gmail.com")
    exe = UserNotInOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]


async def test_get_organization_id() -> None:
    org_name = "okada"
    expected_org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    query = Template(
        """
        query {
            organizationId(organizationName: "$name") {
                id
            }
        }
    """
    )

    data = {"query": query.substitute(name=org_name)}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert result["data"]["organizationId"]["id"] == expected_org_id

    result = await _get_result_async(data, stakeholder="madeupuser@gmail.com")
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    data = {"query": query.substitute(name="madeup-name")}
    result = await _get_result_async(data)
    exe = InvalidOrganization()
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]


async def test_organization() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    expected_groups = ["oneshottest", "unittesting"]
    expected_stakeholders = [
        "continuoushack2@gmail.com",
        "continuoushacking@gmail.com",
        "integratesanalyst@fluidattacks.com",
        "integratescustomer@fluidattacks.com",
        "integratescustomer@gmail.com",
        "integratesexecutive@gmail.com",
        "integratesmanager@fluidattacks.com",
        "integratesmanager@gmail.com",
        "integratesreattacker@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratesreviewer@fluidattacks.com",
        "integratesserviceforces@gmail.com",
        "integratesuser@gmail.com",
        "system_owner@fluidattacks.com",
        "unittest2@fluidattacks.com",
    ]

    variables = {"organizationId": org_id}
    query = """
        query GetOrganizationInfo($organizationId: String!) {
            organization(organizationId: $organizationId) {
                id
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptations
                minAcceptanceSeverity
                name
                groups {
                    name
                }
                stakeholders {
                    email
                }
            }
        }
    """

    data = {"query": query, "variables": variables}
    result = await _get_result_async(data)
    groups = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders = [
        stakeholders["email"]
        for stakeholders in result["data"]["organization"]["stakeholders"]
    ]

    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["maxAcceptanceDays"] == Decimal("60")
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == Decimal(
        "10.0"
    )
    assert result["data"]["organization"]["maxNumberAcceptations"] == Decimal(
        "2"
    )
    assert result["data"]["organization"]["minAcceptanceSeverity"] == Decimal(
        "0.0"
    )
    assert result["data"]["organization"]["name"] == "okada"
    assert sorted(groups) == expected_groups
    assert sorted(stakeholders) == expected_stakeholders

    exe = UserNotInOrganization()
    result = await _get_result_async(data, stakeholder="madeupuser@gmail.com")
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]
