from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (
        ("admin@gmail.com", "admin", 104),
        ("customer@gmail.com", "customer", 47),
        ("customeradmin@gmail.com", "customeradmin", 62),
        ("executive@gmail.com", "executive", 41),
        ("hacker@gmail.com", "hacker", 58),
        ("reattacker@gmail.com", "reattacker", 44),
        ("resourcer@gmail.com", "resourcer", 27),
        ("reviewer@gmail.com", "reviewer", 49),
        ("system_owner@gmail.com", "system_owner", 78),
    ),
)
async def test_get_group(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    group_name: str = "group1"
    consult: str = "This is a test comment"
    finding: str = "475041521"
    event: str = "418900971"
    root: str = "63298a73-9dff-46cf-b42d-9b2f01a56690"
    result: Dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Exception - Document not found"
    assert result["data"]["group"]["name"] == group_name
    assert result["data"]["group"]["hasSquad"]
    assert result["data"]["group"]["hasForces"]
    assert result["data"]["group"]["hasAsm"]
    assert result["data"]["group"]["openVulnerabilities"] == 1
    assert result["data"]["group"]["closedVulnerabilities"] == 1
    assert result["data"]["group"]["lastClosedVulnerability"] == 40
    assert result["data"]["group"]["maxSeverity"] == 4.1
    assert result["data"]["group"]["meanRemediate"] == 2
    assert result["data"]["group"]["meanRemediateCriticalSeverity"] == 0
    assert result["data"]["group"]["meanRemediateHighSeverity"] == 0
    assert result["data"]["group"]["meanRemediateLowSeverity"] == 3
    assert result["data"]["group"]["meanRemediateMediumSeverity"] == 4
    assert result["data"]["group"]["openFindings"] == 1
    assert result["data"]["group"]["totalFindings"] == 1
    assert result["data"]["group"]["totalTreatment"] == "{}"
    assert result["data"]["group"]["subscription"] == "continuous"
    assert result["data"]["group"]["deletionDate"] == ""
    assert result["data"]["group"]["userDeletion"] == ""
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
    assert result["data"]["group"]["maxOpenSeverity"] == 4.3
    assert result["data"]["group"]["maxOpenSeverityFinding"] is None
    assert result["data"]["group"]["lastClosedVulnerabilityFinding"] is None
    assert consult in [
        consult["content"] for consult in result["data"]["group"]["consulting"]
    ]
    assert finding in [
        finding["id"] for finding in result["data"]["group"]["findings"]
    ]
    assert event in [
        event["id"] for event in result["data"]["group"]["events"]
    ]
    assert root in [root["id"] for root in result["data"]["group"]["roots"]]
    assert len(result["data"]["group"]["permissions"]) == permissions
    assert result["data"]["group"]["userRole"] == role


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (("service_forces@gmail.com", "service_forces", 6),),
)
async def test_get_group_fail(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    group_name: str = "group1"
    finding: str = "475041521"
    root: str = "63298a73-9dff-46cf-b42d-9b2f01a56690"
    result: Dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
    assert result["data"]["group"]["name"] == group_name
    assert result["data"]["group"]["hasSquad"]
    assert result["data"]["group"]["hasForces"]
    assert result["data"]["group"]["hasAsm"]
    assert result["data"]["group"]["openVulnerabilities"] == 1
    assert result["data"]["group"]["closedVulnerabilities"] == 1
    assert result["data"]["group"]["lastClosedVulnerability"] == 40
    assert result["data"]["group"]["maxSeverity"] == 4.1
    assert result["data"]["group"]["meanRemediate"] == 2
    assert result["data"]["group"]["meanRemediateCriticalSeverity"] == 0
    assert result["data"]["group"]["meanRemediateHighSeverity"] == 0
    assert result["data"]["group"]["meanRemediateLowSeverity"] == 3
    assert result["data"]["group"]["meanRemediateMediumSeverity"] == 4
    assert result["data"]["group"]["openFindings"] == 1
    assert result["data"]["group"]["totalFindings"] == 1
    assert result["data"]["group"]["totalTreatment"] == "{}"
    assert result["data"]["group"]["subscription"] == "continuous"
    assert result["data"]["group"]["deletionDate"] == ""
    assert result["data"]["group"]["userDeletion"] == ""
    assert result["data"]["group"]["tags"] == ["testing"]
    assert result["data"]["group"]["description"] == "this is group1"
    assert result["data"]["group"]["organization"] == "orgtest"
    assert result["data"]["group"]["userRole"] == email.split("@")[0]
    assert result["data"]["group"]["maxOpenSeverity"] == 4.3
    assert result["data"]["group"]["maxOpenSeverityFinding"] is None
    assert result["data"]["group"]["lastClosedVulnerabilityFinding"] is None
    assert finding in [
        finding["id"] for finding in result["data"]["group"]["findings"]
    ]
    assert root in [root["id"] for root in result["data"]["group"]["roots"]]
    assert len(result["data"]["group"]["permissions"]) == permissions
    assert result["data"]["group"]["userRole"] == role
