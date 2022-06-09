from . import (
    get_result,
    get_vulnerabilities,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)  # pylint: disable=too-many-statements
async def test_get_group(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    consult: str = "This is a test comment"
    finding: str = "475041521"
    event: str = "418900971"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Exception - Document not found"
    assert result["data"]["group"]["name"] == group_name
    assert result["data"]["group"]["hasSquad"]
    assert result["data"]["group"]["hasForces"]
    assert result["data"]["group"]["hasAsm"]
    assert result["data"]["group"]["hasMachine"]
    assert result["data"]["group"]["managed"]
    assert result["data"]["group"]["openVulnerabilities"] == 2
    assert result["data"]["group"]["closedVulnerabilities"] == 1
    assert result["data"]["group"]["lastClosedVulnerability"] == 40
    assert result["data"]["group"]["lastClosedVulnerabilityFinding"] == {
        "id": "475041521"
    }
    assert result["data"]["group"]["maxOpenSeverity"] == 4.3
    assert result["data"]["group"]["maxOpenSeverityFinding"] == {
        "id": "475041521"
    }
    assert result["data"]["group"]["maxSeverity"] == 4.1
    assert result["data"]["group"]["maxSeverityFinding"] == {"id": "475041521"}
    assert result["data"]["group"]["meanRemediate"] == 2
    assert result["data"]["group"]["meanRemediateCriticalSeverity"] is None
    assert result["data"]["group"]["meanRemediateHighSeverity"] is None
    assert result["data"]["group"]["meanRemediateLowSeverity"] == 3
    assert result["data"]["group"]["meanRemediateMediumSeverity"] == 4
    assert result["data"]["group"]["openFindings"] == 2
    assert result["data"]["group"]["totalFindings"] == 2
    assert result["data"]["group"]["totalTreatment"] == "{}"
    assert result["data"]["group"]["subscription"] == "continuous"
    assert result["data"]["group"]["deletionDate"] is None
    assert result["data"]["group"]["userDeletion"] is None
    assert result["data"]["group"]["tags"] == ["testing"]
    assert result["data"]["group"]["description"] == "this is group1"
    assert result["data"]["group"]["serviceAttributes"] == [
        "has_asm",
        "has_forces",
        "has_service_white",
        "has_squad",
        "is_continuous",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    ]
    assert result["data"]["group"]["organization"] == "orgtest"
    assert result["data"]["group"]["userRole"] == email.split("@")[0]
    assert consult in [
        consult["content"] for consult in result["data"]["group"]["consulting"]
    ]
    assert finding in [
        finding["id"] for finding in result["data"]["group"]["findings"]
    ]
    assert event in [
        event["id"] for event in result["data"]["group"]["events"]
    ]
    assert result["data"]["group"]["roots"] == [
        {
            "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "vulnerabilities": [
                {"id": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a"},
                {"id": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6b"},
                {"id": "c188fac2-99b9-483d-8af3-76efbf7715dd"},
            ],
        }
    ]
    assert result["data"]["group"]["language"] == "EN"
    assert result["data"]["group"]["groupContext"] == "This is a dummy context"
    assert result["data"]["group"]["service"] == "WHITE"
    assert result["data"]["group"]["tier"] == "SQUAD"
    assert result["data"]["group"]["businessId"] == "1867"
    assert result["data"]["group"]["businessName"] == "Testing Company"
    assert result["data"]["group"]["sprintDuration"] == 3
    assert result["data"]["group"]["sprintStartDate"] == "2022-06-06T00:00:00"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_group_forces_token(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert result["data"]["group"]["forcesToken"] is not None
    test_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJjaXBABCXYZ"
    assert result["data"]["group"]["forcesToken"] == test_token


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email", "length"],
    [
        ["user@gmail.com", 1],
        ["user_manager@gmail.com", 1],
        ["vulnerability_manager@gmail.com", 1],
    ],
)
async def test_get_assigned(populate: bool, email: str, length: int) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_vulnerabilities(
        user=email, group=group_name
    )
    assert "errors" not in result
    assert len(result["data"]["group"]["vulnerabilitiesAssigned"]) == length
