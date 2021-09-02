from . import (
    get_result,
)
from freezegun import (
    freeze_time,
)
import pytest
from typing import (
    Any,
    Dict,
    List,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)  # pylint: disable=too-many-statements, too-many-locals
@freeze_time("2021-03-31")
async def test_get_finding(populate: bool, email: str) -> None:
    assert populate
    identifier: str = "475041513"
    group_name: str = "group1"
    release_date: str = "2018-04-07 19:45:11"
    severity: Dict[str, float] = {
        "attackComplexity": 0.44,
        "attackVector": 0.2,
        "availabilityImpact": 0.22,
        "availabilityRequirement": 1.5,
        "confidentialityImpact": 0.22,
        "confidentialityRequirement": 0.5,
        "exploitability": 0.94,
        "integrityImpact": 0.22,
        "integrityRequirement": 1.0,
        "modifiedAttackComplexity": 0.44,
        "modifiedAttackVector": 0.85,
        "modifiedAvailabilityImpact": 0.22,
        "modifiedConfidentialityImpact": 0.22,
        "modifiedIntegrityImpact": 0.0,
        "modifiedPrivilegesRequired": 0.27,
        "modifiedUserInteraction": 0.62,
        "modifiedSeverityScope": 0.0,
        "privilegesRequired": 0.62,
        "remediationLevel": 0.95,
        "reportConfidence": 1.0,
        "severityScope": 1.2,
        "userInteraction": 0.85,
    }
    cvss_version: str = "3.1"
    state: str = "open"
    last_vuln: int = 1087
    remediated: bool = False
    age: int = 1087
    is_exploitable: bool = False
    severity_score: float = 4.1
    report_date: str = ""
    analyst: str = "test1@gmail.com"
    historic_state: List[Any] = [
        {
            "date": release_date,
            "analyst": analyst,
            "source": "source_path",
            "state": "APPROVED",
        }
    ]
    current_state: str = "APPROVED"
    new_remediated: bool = False
    verified: bool = True
    ports_vulnerabilities: List[Any] = [
        {"specific": "2321"},
        {"specific": "9999"},
    ]
    inputs_vulnerabilities: List[Any] = []
    lines_vulnerabilities: List[Any] = []
    open_vuln: str = "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a"
    closed_vuln: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    finding_id: str = "475041513"
    title: str = "001. SQL injection - C Sharp SQL API"
    scenario: str = "UNAUTHORIZED_USER_EXTRANET"
    actor: str = "ANYONE_INTERNET"
    description: str = "I just have updated the description"
    requirements: str = (
        "REQ.0132. Passwords (phrase type) must be at least 3 words long."
    )
    attack_vector_description: str = "This is an updated attack vector"
    threat: str = "Updated threat"
    recommendation: str = "Updated recommendation"
    affected_systems: str = "Server bWAPP"
    records: str = "Clave plana"
    records_number: int = 12
    risk: str = "This is pytest created draft"
    finding_type: str = "SECURITY"
    tracking: Dict[str, Any] = {
        "tracking": [
            {
                "cycle": 0,
                "open": 1,
                "closed": 0,
                "date": "2018-04-07",
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": "",
                "justification": "",
            },
            {
                "cycle": 1,
                "open": 0,
                "closed": 1,
                "date": "2018-04-07",
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": "",
                "justification": "",
            },
            {
                "cycle": 2,
                "open": 0,
                "closed": 0,
                "date": "2018-04-08",
                "accepted": 1,
                "accepted_undefined": 0,
                "manager": "anything@gmail.com",
                "justification": "justification",
            },
        ]
    }
    treatment_summary: Dict[str, int] = {
        "accepted": 1,
        "acceptedUndefined": 0,
        "inProgress": 0,
        "new": 0,
    }
    where: str = "192.168.1.1"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
    )
    assert "errors" not in result
    assert result["data"]["finding"]["id"] == identifier
    assert result["data"]["finding"]["groupName"] == group_name
    assert result["data"]["finding"]["releaseDate"] == release_date
    assert result["data"]["finding"]["severity"] == severity
    assert result["data"]["finding"]["cvssVersion"] == cvss_version
    assert result["data"]["finding"]["state"] == state
    assert result["data"]["finding"]["lastVulnerability"] == last_vuln
    assert result["data"]["finding"]["remediated"] == remediated
    assert result["data"]["finding"]["age"] == age
    assert result["data"]["finding"]["isExploitable"] == is_exploitable
    assert result["data"]["finding"]["severityScore"] == severity_score
    assert result["data"]["finding"]["reportDate"] == report_date
    assert result["data"]["finding"]["historicState"] == historic_state
    assert result["data"]["finding"]["currentState"] == current_state
    assert result["data"]["finding"]["newRemediated"] == new_remediated
    assert result["data"]["finding"]["verified"] == verified
    assert result["data"]["finding"]["analyst"] == analyst
    assert (
        result["data"]["finding"]["portsVulnerabilities"]
        == ports_vulnerabilities
    )
    assert (
        result["data"]["finding"]["inputsVulnerabilities"]
        == inputs_vulnerabilities
    )
    assert (
        result["data"]["finding"]["linesVulnerabilities"]
        == lines_vulnerabilities
    )
    vuln_ids: List[str] = [
        vuln["id"] for vuln in result["data"]["finding"]["vulnerabilities"]
    ]
    assert open_vuln in vuln_ids
    assert closed_vuln in vuln_ids
    assert result["data"]["finding"]["openVulnerabilities"] == 1
    assert result["data"]["finding"]["closedVulnerabilities"] == 1
    assert len(result["data"]["finding"]["evidence"]) == 7
    assert result["data"]["finding"]["evidence"]["evidence2"]["url"] == ""
    assert (
        f"group1-{finding_id}"
        in result["data"]["finding"]["evidence"]["animation"]["url"]
    )
    assert result["data"]["finding"]["title"] == title
    assert result["data"]["finding"]["scenario"] == scenario
    assert result["data"]["finding"]["actor"] == actor
    assert result["data"]["finding"]["description"] == description
    assert result["data"]["finding"]["requirements"] == requirements
    assert (
        result["data"]["finding"]["attackVectorDescription"]
        == attack_vector_description
    )
    assert result["data"]["finding"]["threat"] == threat
    assert result["data"]["finding"]["recommendation"] == recommendation
    assert result["data"]["finding"]["affectedSystems"] == affected_systems
    assert result["data"]["finding"]["compromisedAttributes"] == records
    assert result["data"]["finding"]["compromisedRecords"] == records_number
    assert result["data"]["finding"]["bugTrackingSystemUrl"] == ""
    assert result["data"]["finding"]["risk"] == risk
    assert result["data"]["finding"]["type"] == finding_type
    assert result["data"]["finding"]["observations"] == []
    assert result["data"]["finding"]["consulting"] == []
    assert result["data"]["finding"]["tracking"] == tracking.get("tracking")
    assert result["data"]["finding"]["where"] == where
    assert result["data"]["finding"]["treatmentSummary"] == treatment_summary


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["group_manager@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)  # pylint: disable=too-many-statements, too-many-locals
@freeze_time("2021-03-31")
async def test_get_finding_fail(populate: bool, email: str) -> None:
    assert populate
    identifier: str = "475041513"
    group_name: str = "group1"
    release_date: str = "2018-04-07 19:45:11"
    severity: Dict[str, float] = {
        "attackComplexity": 0.44,
        "attackVector": 0.2,
        "availabilityImpact": 0.22,
        "availabilityRequirement": 1.5,
        "confidentialityImpact": 0.22,
        "confidentialityRequirement": 0.5,
        "exploitability": 0.94,
        "integrityImpact": 0.22,
        "integrityRequirement": 1.0,
        "modifiedAttackComplexity": 0.44,
        "modifiedAttackVector": 0.85,
        "modifiedAvailabilityImpact": 0.22,
        "modifiedConfidentialityImpact": 0.22,
        "modifiedIntegrityImpact": 0.0,
        "modifiedPrivilegesRequired": 0.27,
        "modifiedUserInteraction": 0.62,
        "modifiedSeverityScope": 0.0,
        "privilegesRequired": 0.62,
        "remediationLevel": 0.95,
        "reportConfidence": 1.0,
        "severityScope": 1.2,
        "userInteraction": 0.85,
    }
    cvss_version: str = "3.1"
    state: str = "open"
    last_vuln: int = 1087
    remediated: bool = False
    age: int = 1087
    is_exploitable: bool = False
    severity_score: float = 4.1
    report_date: str = ""
    current_state: str = "APPROVED"
    new_remediated: bool = False
    verified: bool = True
    ports_vulnerabilities: List[Any] = [
        {"specific": "2321"},
        {"specific": "9999"},
    ]
    inputs_vulnerabilities: List[Any] = []
    lines_vulnerabilities: List[Any] = []
    open_vuln: str = "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a"
    closed_vuln: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    finding_id: str = "475041513"
    title: str = "001. SQL injection - C Sharp SQL API"
    scenario: str = "UNAUTHORIZED_USER_EXTRANET"
    actor: str = "ANYONE_INTERNET"
    description: str = "I just have updated the description"
    requirements: str = (
        "REQ.0132. Passwords (phrase type) must be at least 3 words long."
    )
    attack_vector_description: str = "This is an updated attack vector"
    threat: str = "Updated threat"
    recommendation: str = "Updated recommendation"
    affected_systems: str = "Server bWAPP"
    records: str = "Clave plana"
    records_number: int = 12
    risk: str = "This is pytest created draft"
    finding_type: str = "SECURITY"
    tracking: Dict[str, Any] = {
        "tracking": [
            {
                "cycle": 0,
                "open": 1,
                "closed": 0,
                "date": "2018-04-07",
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": "",
                "justification": "",
            },
            {
                "cycle": 1,
                "open": 0,
                "closed": 1,
                "date": "2018-04-07",
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": "",
                "justification": "",
            },
            {
                "cycle": 2,
                "open": 0,
                "closed": 0,
                "date": "2018-04-08",
                "accepted": 1,
                "accepted_undefined": 0,
                "manager": "anything@gmail.com",
                "justification": "justification",
            },
        ]
    }
    treatment_summary: Dict[str, int] = {
        "accepted": 1,
        "acceptedUndefined": 0,
        "inProgress": 0,
        "new": 0,
    }
    where: str = "192.168.1.1"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
    )
    assert "errors" in result
    assert result["data"]["finding"]["id"] == identifier
    assert result["data"]["finding"]["groupName"] == group_name
    assert result["data"]["finding"]["releaseDate"] == release_date
    assert result["data"]["finding"]["severity"] == severity
    assert result["data"]["finding"]["cvssVersion"] == cvss_version
    assert result["data"]["finding"]["state"] == state
    assert result["data"]["finding"]["lastVulnerability"] == last_vuln
    assert result["data"]["finding"]["remediated"] == remediated
    assert result["data"]["finding"]["age"] == age
    assert result["data"]["finding"]["isExploitable"] == is_exploitable
    assert result["data"]["finding"]["severityScore"] == severity_score
    assert result["data"]["finding"]["reportDate"] == report_date
    assert result["data"]["finding"]["currentState"] == current_state
    assert result["data"]["finding"]["newRemediated"] == new_remediated
    assert result["data"]["finding"]["verified"] == verified
    assert (
        result["data"]["finding"]["portsVulnerabilities"]
        == ports_vulnerabilities
    )
    assert (
        result["data"]["finding"]["inputsVulnerabilities"]
        == inputs_vulnerabilities
    )
    assert (
        result["data"]["finding"]["linesVulnerabilities"]
        == lines_vulnerabilities
    )
    vuln_ids: List[str] = [
        vuln["id"] for vuln in result["data"]["finding"]["vulnerabilities"]
    ]
    assert open_vuln in vuln_ids
    assert closed_vuln in vuln_ids
    assert result["data"]["finding"]["openVulnerabilities"] == 1
    assert result["data"]["finding"]["closedVulnerabilities"] == 1
    assert len(result["data"]["finding"]["evidence"]) == 7
    assert result["data"]["finding"]["evidence"]["evidence2"]["url"] == ""
    assert (
        f"group1-{finding_id}"
        in result["data"]["finding"]["evidence"]["animation"]["url"]
    )
    assert result["data"]["finding"]["title"] == title
    assert result["data"]["finding"]["scenario"] == scenario
    assert result["data"]["finding"]["actor"] == actor
    assert result["data"]["finding"]["description"] == description
    assert result["data"]["finding"]["requirements"] == requirements
    assert (
        result["data"]["finding"]["attackVectorDescription"]
        == attack_vector_description
    )
    assert result["data"]["finding"]["threat"] == threat
    assert result["data"]["finding"]["recommendation"] == recommendation
    assert result["data"]["finding"]["affectedSystems"] == affected_systems
    assert result["data"]["finding"]["compromisedAttributes"] == records
    assert result["data"]["finding"]["compromisedRecords"] == records_number
    assert result["data"]["finding"]["bugTrackingSystemUrl"] == ""
    assert result["data"]["finding"]["risk"] == risk
    assert result["data"]["finding"]["type"] == finding_type
    assert result["data"]["finding"]["tracking"] == tracking.get("tracking")
    assert result["data"]["finding"]["where"] == where
    assert result["data"]["finding"]["treatmentSummary"] == treatment_summary
