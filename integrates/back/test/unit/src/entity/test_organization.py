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
from custom_exceptions import (
    InvalidOrganization,
    OrganizationNotFound,
    StakeholderNotInOrganization,
)
from dataloaders import (
    apply_context_attrs,
)
from decimal import (
    Decimal,
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
    request = apply_context_attrs(request)  # type: ignore
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


@pytest.mark.changes_db
async def test_add_organization() -> None:
    stakeholder = "admin@fluidattacks.com"
    mutation_tpl = Template(
        """
        mutation {
            addOrganization(country: "Colombia", name: "$name") {
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
    result = await _get_result_async(data, stakeholder)

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
    exe = InvalidOrganization("Invalid name")
    result = await _get_result_async(data, stakeholder)
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
                maxNumberAcceptances: 3,
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
    exe = StakeholderNotInOrganization()
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
    exe = OrganizationNotFound()
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]


async def test_organization() -> None:
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    expected_groups = ["oneshottest", "unittesting"]
    expected_stakeholders = [
        "continuoushack2@gmail.com",
        "continuoushacking@gmail.com",
        "customer_manager@fluidattacks.com",
        "forces.unittesting@fluidattacks.com",
        "integratesuser2@fluidattacks.com",
        "integratesuser2@gmail.com",
        "integrateshacker@fluidattacks.com",
        "integratesmanager@fluidattacks.com",
        "integratesmanager@gmail.com",
        "integratesreattacker@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratesreviewer@fluidattacks.com",
        "integratesserviceforces@fluidattacks.com",
        "integratesuser@gmail.com",
        "unittest2@fluidattacks.com",
    ]

    variables = {"organizationId": org_id}
    query = """
        query GetOrganizationInfo($organizationId: String!) {
            organization(organizationId: $organizationId) {
                company {
                    domain
                    trial {
                        completed
                    }
                }
                id
                maxAcceptanceDays
                maxAcceptanceSeverity
                maxNumberAcceptances
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
    assert result["data"]["organization"]["maxNumberAcceptances"] == Decimal(
        "2"
    )
    assert result["data"]["organization"]["minAcceptanceSeverity"] == Decimal(
        "0.0"
    )
    assert result["data"]["organization"]["name"] == "okada"
    assert sorted(groups) == expected_groups
    for stakeholder in expected_stakeholders:
        assert stakeholder in stakeholders
    assert result["data"]["organization"]["company"] == {
        "domain": "unknown.com",
        "trial": {"completed": True},
    }

    exe = StakeholderNotInOrganization()
    result = await _get_result_async(data, stakeholder="madeupuser@gmail.com")
    assert "errors" in result
    assert result["errors"][0]["message"] == exe.args[0]
