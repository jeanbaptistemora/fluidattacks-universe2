# pylint: disable=too-many-arguments, import-error
from . import (
    get_stakeholders,
    get_vulnerabilities_assigned,
    get_vulnerability,
    grant_stakeholder,
    put_mutation,
)
from asyncio import (
    sleep,
)
from back.test.functional.src.update_group_policies import (
    update_group_policies,
)
from back.test.functional.src.update_organization_policies import (
    get_result as update_organization_policies,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAssigned,
    VulnAlreadyClosed,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.utils import (
    get_inverted_treatment_converted,
)
from findings.domain.core import (
    get_severity_score,
)
from freezegun import (
    freeze_time,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    (
        "email",
        "vulnerability",
        "treatment",
        "assigned",
        "acceptance_date",
        "current",
    ),
    (
        (
            "user@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            {
                "acceptanceDate": None,
                "acceptanceStatus": None,
                "justification": (
                    "test of update vulns treatment justification"
                ),
                "date": "",
                "treatment": "IN_PROGRESS",
                "user": "user@gmail.com",
            },
            "user@gmail.com",
            "",
            "NEW",
        ),
        (
            "user_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            {
                "acceptanceDate": None,
                "acceptanceStatus": "SUBMITTED",
                "justification": (
                    "test of update vulns treatment justification"
                ),
                "date": "",
                "treatment": "ACCEPTED_UNDEFINED",
                "user": "user_manager@gmail.com",
            },
            "user@gmail.com",
            "",
            "ACCEPTED_UNDEFINED",
        ),
        (
            "user_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc10",
            {
                "acceptanceStatus": None,
                "justification": (
                    "test of update vulns treatment justification"
                ),
                "date": "",
                "treatment": "ACCEPTED",
                "user": "user_manager@fluidattacks.com",
            },
            "user@gmail.com",
            "2021-03-31 19:45:11",
            "ACCEPTED_UNDEFINED",
        ),
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc11",
            {
                "acceptanceStatus": None,
                "justification": (
                    "test of update vulns treatment justification"
                ),
                "date": "",
                "treatment": "ACCEPTED",
                "user": "vulnerability_manager@gmail.com",
            },
            "user@gmail.com",
            "2021-03-31 19:45:11",
            "ACCEPTED_UNDEFINED",
        ),
        (
            "user_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc11",
            {
                "acceptanceStatus": None,
                "justification": (
                    "test of update vulns treatment justification"
                ),
                "date": "",
                "treatment": "ACCEPTED",
                "user": "user_manager@fluidattacks.com",
            },
            "user@fluidattacks.com",
            "2021-03-31 19:45:11",
            "ACCEPTED",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: dict,
    assigned: str,
    acceptance_date: str,
    current: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vulnerability_response: dict = await get_vulnerability(
        user=email, vulnerability_id=vulnerability
    )

    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["treatment"]
        == current
    )
    assert vulnerability_response["data"]["vulnerability"][
        "historicTreatmentStatus"
    ][-1]["treatment"] == get_inverted_treatment_converted(current)

    result: dict = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment["treatment"],
        assigned=assigned,
        acceptance_date=acceptance_date,
    )
    await sleep(5)
    assert "errors" not in result
    assert result["data"]["updateVulnerabilitiesTreatment"]["success"]

    vulnerability_response = await get_vulnerability(
        user=email, vulnerability_id=vulnerability
    )

    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["assigned"]
        == assigned
    )
    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["acceptanceStatus"]
        == treatment["acceptanceStatus"]
    )
    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["justification"]
        == treatment["justification"]
    )
    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["user"]
        == treatment["user"]
    )
    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["treatment"]
        == treatment["treatment"]
    )
    assert (
        vulnerability_response["data"]["vulnerability"][
            "historicTreatmentStatus"
        ][-1]["assigned"]
        == assigned
    )
    assert vulnerability_response["data"]["vulnerability"][
        "historicTreatmentStatus"
    ][-1]["treatment"] == get_inverted_treatment_converted(
        treatment["treatment"]
    )
    assert (
        vulnerability_response["data"]["vulnerability"][
            "historicTreatmentStatus"
        ][-1]["acceptanceStatus"]
        == treatment["acceptanceStatus"]
    )
    assert (
        vulnerability_response["data"]["vulnerability"][
            "historicTreatmentStatus"
        ][-1]["justification"]
        == treatment["justification"]
    )
    assert (
        vulnerability_response["data"]["vulnerability"][
            "historicTreatmentStatus"
        ][-1]["user"]
        == treatment["user"]
    )

    result = await get_vulnerabilities_assigned(user=assigned)
    vuln_ids = [
        vuln["id"] for vuln in result["data"]["me"]["vulnerabilitiesAssigned"]
    ]
    assert vulnerability in vuln_ids


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment", "assigned", "acceptance_date"),
    (
        (
            "user@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc11",
            "ACCEPTED",
            "user_manager@gmail.com",
            "2021-03-31 19:45:11",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment_non_manager(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
    acceptance_date: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date=acceptance_date,
    )
    assert "errors" not in result
    assert result["data"]["updateVulnerabilitiesTreatment"]["success"]
    vulnerability_response: dict[str, Any] = await get_vulnerability(
        user=email, vulnerability_id=vulnerability
    )
    assert (
        vulnerability_response["data"]["vulnerability"]["historicTreatment"][
            -1
        ]["assigned"]
        == email
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment", "assigned", "acceptance_date"),
    (
        (
            "vulnerability_manager@gmail.com",
            "b7ae9350-a94e-40a9-a35f-a3dcee93c959",
            "ACCEPTED",
            "user@gmail.com",
            "2021-03-31 19:45:11",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment_closed(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
    acceptance_date: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date=acceptance_date,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(VulnAlreadyClosed())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment", "assigned"),
    (
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc11",
            "ACCEPTED",
            "user@gmail.com",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment_invalid_organization_policies(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)

    result_1: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="2021-04-02 19:45:11",
    )
    assert "errors" not in result_1
    assert result_1["data"]["updateVulnerabilitiesTreatment"]["success"]

    update_policies_1: dict[str, Any] = await update_organization_policies(
        user="admin@gmail.com",
        organization_id=org_id,
        organization_name=org_name,
        inactivity_period=90,
        max_acceptance_days=5,
        max_acceptance_severity=4.9,
        max_number_acceptances=5,
        min_acceptance_severity=0.0,
        min_breaking_severity=5.9,
        vulnerability_grace_period=10,
    )
    assert "errors" not in update_policies_1
    assert update_policies_1["data"]["updateOrganizationPolicies"]["success"]

    result_2: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="2021-05-11 19:45:11",
    )
    assert "errors" in result_2
    assert result_2["errors"][0]["message"] == str(
        InvalidAcceptanceDays(
            "Chosen date is either in the past or exceeds "
            "the maximum number of days allowed by the defined policy"
        )
    )

    update_policies_2: dict[str, Any] = await update_organization_policies(
        user="admin@gmail.com",
        organization_id=org_id,
        organization_name=org_name,
        inactivity_period=90,
        max_acceptance_days=120,
        max_acceptance_severity=3.9,
        max_number_acceptances=5,
        min_acceptance_severity=0.0,
        min_breaking_severity=5.9,
        vulnerability_grace_period=10,
    )
    assert "errors" not in update_policies_2
    assert update_policies_2["data"]["updateOrganizationPolicies"]["success"]

    result_3: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="2021-05-21 19:45:11",
    )
    assert "errors" in result_3
    assert result_3["errors"][0]["message"] == str(
        InvalidAcceptanceSeverity(str(get_severity_score(finding.severity)))
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment", "assigned"),
    (
        (
            "vulnerability_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc11",
            "ACCEPTED",
            "user@gmail.com",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment_invalid_group_policies(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    group_name: str = "group1"
    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)

    organization_policies: dict[str, Any] = await update_organization_policies(
        user="admin@gmail.com",
        organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
        organization_name="orgtest",
        inactivity_period=90,
        max_acceptance_days=7,
        max_acceptance_severity=10.0,
        max_number_acceptances=30,
        min_acceptance_severity=0.0,
        min_breaking_severity=0.0,
        vulnerability_grace_period=5,
    )
    assert "errors" not in organization_policies
    assert organization_policies["data"]["updateOrganizationPolicies"][
        "success"
    ]

    result_1: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="2021-04-02 19:45:11",
    )
    assert "errors" not in result_1
    assert result_1["data"]["updateVulnerabilitiesTreatment"]["success"]

    update_policies_1: dict[str, Any] = await update_group_policies(
        group_name=group_name,
        max_acceptance_days=5,
        max_acceptance_severity=4.9,
        max_number_acceptances=5,
        min_acceptance_severity=0.0,
        min_breaking_severity=5.9,
        vulnerability_grace_period=10,
        user="admin@gmail.com",
    )
    assert "errors" not in update_policies_1
    assert update_policies_1["data"]["updateGroupPolicies"]["success"]

    result_2: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="2021-05-11 19:45:11",
    )
    assert "errors" in result_2
    assert result_2["errors"][0]["message"] == str(
        InvalidAcceptanceDays(
            "Chosen date is either in the past or exceeds "
            "the maximum number of days allowed by the defined policy"
        )
    )

    update_policies_2: dict[str, Any] = await update_group_policies(
        group_name=group_name,
        max_acceptance_days=120,
        max_acceptance_severity=3.9,
        max_number_acceptances=5,
        min_acceptance_severity=0.0,
        min_breaking_severity=5.9,
        user="admin@gmail.com",
        vulnerability_grace_period=10,
    )
    assert "errors" not in update_policies_2
    assert update_policies_2["data"]["updateGroupPolicies"]["success"]

    result_3: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="2021-05-21 19:45:11",
    )
    assert "errors" in result_3
    assert result_3["errors"][0]["message"] == str(
        InvalidAcceptanceSeverity(str(get_severity_score(finding.severity)))
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment"),
    (
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "reviewer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "customer_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment_fail(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=email,
        acceptance_date="2021-03-31 19:45:11",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment", "assigned"),
    (
        (
            "user_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "IN_PROGRESS",
            "nonconfirmeduser@test.com",
        ),
    ),
)
async def test_update_vulnerabilities_treatment_non_confirmed(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    group_name: str = "group1"
    result_grant: dict[str, Any] = await grant_stakeholder(
        user=email,
        stakeholder=assigned,
        group=group_name,
    )
    assert "errors" not in result_grant
    assert result_grant["data"]["grantStakeholderAccess"]["success"]

    stakeholders: dict[str, Any] = await get_stakeholders(
        user=email, group=group_name
    )
    for stakeholder in stakeholders["data"]["group"]["stakeholders"]:
        if stakeholder["email"] == assigned:
            assert stakeholder["invitationState"] == "PENDING"

    result: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidAssigned())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment", "assigned"),
    (
        (
            "user_manager@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "IN_PROGRESS",
            "user@fluidattacks.com",
        ),
    ),
)
async def test_update_vulnerabilities_treatment_invalid_assigned_fail(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
    assigned: str,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: dict[str, Any] = await put_mutation(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
        assigned=assigned,
        acceptance_date="",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidAssigned())
