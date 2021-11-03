from . import (
    get_result,
)
from freezegun import (  # type: ignore
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
        ["admin@fluidattacks.com"],
    ],
)  # pylint: disable=too-many-statements, too-many-locals
@freeze_time("2021-03-31")
async def test_get_finding(populate: bool, email: str) -> None:
    assert populate
    identifier: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    group_name: str = "group1"
    historic_state = [
        {
            "analyst": "test1@gmail.com",
            "date": "2017-04-07 19:45:11",
            "source": "asm",
            "state": "CREATED",
        },
        {
            "analyst": "test1@gmail.com",
            "date": "2017-04-07 19:45:12",
            "source": "asm",
            "state": "SUBMITTED",
        },
        {
            "analyst": "test1@gmail.com",
            "date": "2017-04-07 19:45:13",
            "source": "asm",
            "state": "REJECTED",
        },
        {
            "analyst": "test1@gmail.com",
            "date": "2017-04-07 19:45:14",
            "source": "asm",
            "state": "SUBMITTED",
        },
        {
            "analyst": "test1@gmail.com",
            "date": "2018-04-07 19:45:11",
            "source": "asm",
            "state": "APPROVED",
        },
    ]
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
    last_vuln: int = 94
    remediated: bool = False
    age: int = 1094
    open_age: int = 400
    is_exploitable: bool = False
    severity_score: float = 4.1
    report_date: str = "2018-04-01 00:45:00"
    hacker: str = "test1@gmail.com"
    current_state: str = "APPROVED"
    verified: bool = False
    ports_vulnerabilities: List[Any] = [
        {"specific": "2321"},
        {"specific": "77777"},
        {"specific": "9999"},
    ]
    inputs_vulnerabilities: List[Any] = []
    lines_vulnerabilities: List[Any] = []
    open_vuln: str = "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a"
    closed_vuln: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    title: str = "001. SQL injection - C Sharp SQL API"
    description: str = "I just have updated the description"
    requirements: str = (
        "REQ.0132. Passwords (phrase type) must be at least 3 words long."
    )
    attack_vector_description: str = "This is an updated attack vector"
    threat: str = "Updated threat"
    recommendation: str = "Updated recommendation"
    affected_systems: str = "Server bWAPP"
    tracking: List[Dict[str, Any]] = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2018-04-07",
            "accepted": 0,
            "acceptedUndefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 0,
            "closed": 1,
            "date": "2018-04-07",
            "accepted": 0,
            "acceptedUndefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 0,
            "closed": 0,
            "date": "2018-04-08",
            "accepted": 1,
            "acceptedUndefined": 0,
            "manager": "anything@gmail.com",
            "justification": "justification",
        },
    ]
    treatment_summary: Dict[str, int] = {
        "accepted": 1,
        "acceptedUndefined": 2,
        "inProgress": 3,
        "new": 4,
    }
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    where: str = "192.168.1.2"
    assert "errors" not in result
    assert result["data"]["finding"]["affectedSystems"] == affected_systems
    assert result["data"]["finding"]["age"] == age
    assert result["data"]["finding"]["hacker"] == hacker
    assert (
        result["data"]["finding"]["attackVectorDesc"]
        == attack_vector_description
    )
    assert (
        result["data"]["finding"]["attackVectorDescription"]
        == attack_vector_description
    )
    assert result["data"]["finding"]["closedVulnerabilities"] == 3
    assert result["data"]["finding"]["consulting"] == [
        {
            "content": (
                "Regarding vulnerabilities 192.168.1.20:\n\n"
                "This is a test observations"
            )
        },
    ]
    assert result["data"]["finding"]["currentState"] == current_state
    assert result["data"]["finding"]["cvssVersion"] == cvss_version
    assert result["data"]["finding"]["description"] == description
    assert len(result["data"]["finding"]["evidence"]) == 7
    assert (
        result["data"]["finding"]["evidence"]["evidence2"]["url"]
        == "group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence2"
    )
    assert (
        f"group1-{finding_id}"
        in result["data"]["finding"]["evidence"]["animation"]["url"]
    )
    assert result["data"]["finding"]["groupName"] == group_name
    assert result["data"]["finding"]["historicState"] == historic_state
    assert result["data"]["finding"]["id"] == identifier
    assert result["data"]["finding"]["inputsVulns"] == inputs_vulnerabilities
    assert (
        result["data"]["finding"]["inputsVulnerabilities"]
        == inputs_vulnerabilities
    )
    assert result["data"]["finding"]["isExploitable"] == is_exploitable
    assert result["data"]["finding"]["lastVulnerability"] == last_vuln
    assert result["data"]["finding"]["linesVulns"] == lines_vulnerabilities
    assert (
        result["data"]["finding"]["linesVulnerabilities"]
        == lines_vulnerabilities
    )
    assert result["data"]["finding"]["newRemediated"] == remediated
    assert result["data"]["finding"]["observations"] == [
        {"content": "This is a test observations"}
    ]
    assert result["data"]["finding"]["openAge"] == open_age
    assert result["data"]["finding"]["openVulnerabilities"] == 5
    assert result["data"]["finding"]["portsVulns"] == ports_vulnerabilities
    assert (
        result["data"]["finding"]["portsVulnerabilities"]
        == ports_vulnerabilities
    )
    assert result["data"]["finding"]["projectName"] == group_name
    assert result["data"]["finding"]["recommendation"] == recommendation
    assert result["data"]["finding"]["records"] == "[]"
    assert result["data"]["finding"]["releaseDate"] == release_date
    assert result["data"]["finding"]["remediated"] == remediated
    assert result["data"]["finding"]["reportDate"] == report_date
    assert result["data"]["finding"]["requirements"] == requirements
    assert result["data"]["finding"]["severity"] == severity
    assert result["data"]["finding"]["severityScore"] == severity_score
    assert result["data"]["finding"]["sorts"] == "NO"
    assert result["data"]["finding"]["state"] == state
    assert result["data"]["finding"]["threat"] == threat
    assert result["data"]["finding"]["title"] == title
    assert result["data"]["finding"]["tracking"] == tracking
    assert result["data"]["finding"]["treatmentSummary"] == treatment_summary
    assert result["data"]["finding"]["verified"] == verified
    assert result["data"]["finding"]["vulnsToReattack"] == []
    assert result["data"]["finding"]["vulnerabilitiesToReattack"] == []
    vuln_ids: List[str] = [
        vuln["id"] for vuln in result["data"]["finding"]["vulnerabilities"]
    ]
    assert open_vuln in vuln_ids
    assert closed_vuln in vuln_ids
    assert result["data"]["finding"]["zeroRisk"] == [
        {"id": "7771bc87-8633-4a4a-8d8e-7dae0ca57e7a"}
    ]
    assert result["data"]["finding"]["where"] == where


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@fluidattacks.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)  # pylint: disable=too-many-statements, too-many-locals
@freeze_time("2021-03-31")
async def test_get_finding_fail(populate: bool, email: str) -> None:
    assert populate
    identifier: str = "3c475384-834c-47b0-ac71-a41a022e401c"
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
    last_vuln: int = 94
    remediated: bool = False
    age: int = 1094
    open_age: int = 400
    is_exploitable: bool = False
    severity_score: float = 4.1
    report_date: str = "2018-04-01 00:45:00"
    current_state: str = "APPROVED"
    new_remediated: bool = False
    verified: bool = False
    ports_vulnerabilities: List[Any] = [
        {"specific": "2321"},
        {"specific": "77777"},
        {"specific": "9999"},
    ]
    inputs_vulnerabilities: List[Any] = []
    lines_vulnerabilities: List[Any] = []
    open_vuln: str = "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a"
    closed_vuln: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    title: str = "001. SQL injection - C Sharp SQL API"
    description: str = "I just have updated the description"
    requirements: str = (
        "REQ.0132. Passwords (phrase type) must be at least 3 words long."
    )
    attack_vector_description: str = "This is an updated attack vector"
    threat: str = "Updated threat"
    recommendation: str = "Updated recommendation"
    affected_systems: str = "Server bWAPP"
    tracking: List[Dict[str, Any]] = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2018-04-07",
            "accepted": 0,
            "acceptedUndefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 0,
            "closed": 1,
            "date": "2018-04-07",
            "accepted": 0,
            "acceptedUndefined": 0,
            "manager": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 0,
            "closed": 0,
            "date": "2018-04-08",
            "accepted": 1,
            "acceptedUndefined": 0,
            "manager": "anything@gmail.com",
            "justification": "justification",
        },
    ]
    treatment_summary: Dict[str, int] = {
        "accepted": 1,
        "acceptedUndefined": 2,
        "inProgress": 3,
        "new": 4,
    }
    where: str = "192.168.1.2"
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" in result
    assert result["data"]["finding"]["affectedSystems"] == affected_systems
    assert result["data"]["finding"]["age"] == age
    assert (
        result["data"]["finding"]["attackVectorDesc"]
        == attack_vector_description
    )
    assert (
        result["data"]["finding"]["attackVectorDescription"]
        == attack_vector_description
    )
    assert result["data"]["finding"]["closedVulnerabilities"] == 3
    assert result["data"]["finding"]["consulting"] == [
        {
            "content": (
                "Regarding vulnerabilities 192.168.1.20:\n\n"
                "This is a test observations"
            )
        },
    ]
    assert result["data"]["finding"]["currentState"] == current_state
    assert result["data"]["finding"]["cvssVersion"] == cvss_version
    assert result["data"]["finding"]["description"] == description
    assert len(result["data"]["finding"]["evidence"]) == 7
    assert (
        result["data"]["finding"]["evidence"]["evidence2"]["url"]
        == "group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence2"
    )
    assert (
        f"group1-{finding_id}"
        in result["data"]["finding"]["evidence"]["animation"]["url"]
    )
    assert result["data"]["finding"]["groupName"] == group_name
    assert result["data"]["finding"]["id"] == identifier
    assert result["data"]["finding"]["inputsVulns"] == inputs_vulnerabilities
    assert (
        result["data"]["finding"]["inputsVulnerabilities"]
        == inputs_vulnerabilities
    )
    assert result["data"]["finding"]["isExploitable"] == is_exploitable
    assert result["data"]["finding"]["lastVulnerability"] == last_vuln
    assert result["data"]["finding"]["linesVulns"] == lines_vulnerabilities
    assert (
        result["data"]["finding"]["linesVulnerabilities"]
        == lines_vulnerabilities
    )
    assert result["data"]["finding"]["newRemediated"] == new_remediated
    assert result["data"]["finding"]["openAge"] == open_age
    assert result["data"]["finding"]["openVulnerabilities"] == 5
    assert (
        result["data"]["finding"]["portsVulnerabilities"]
        == ports_vulnerabilities
    )
    assert result["data"]["finding"]["projectName"] == group_name
    assert result["data"]["finding"]["recommendation"] == recommendation
    assert result["data"]["finding"]["records"] == "[]"
    assert result["data"]["finding"]["releaseDate"] == release_date
    assert result["data"]["finding"]["remediated"] == remediated
    assert result["data"]["finding"]["reportDate"] == report_date
    assert result["data"]["finding"]["requirements"] == requirements
    assert result["data"]["finding"]["severity"] == severity
    assert result["data"]["finding"]["severityScore"] == severity_score
    assert result["data"]["finding"]["state"] == state
    assert result["data"]["finding"]["threat"] == threat
    assert result["data"]["finding"]["title"] == title
    assert result["data"]["finding"]["tracking"] == tracking
    assert result["data"]["finding"]["treatmentSummary"] == treatment_summary
    assert result["data"]["finding"]["verified"] == verified
    assert result["data"]["finding"]["vulnsToReattack"] == []
    assert result["data"]["finding"]["vulnerabilitiesToReattack"] == []
    vuln_ids: List[str] = [
        vuln["id"] for vuln in result["data"]["finding"]["vulnerabilities"]
    ]
    assert result["data"]["finding"]["where"] == where
    assert open_vuln in vuln_ids
    assert closed_vuln in vuln_ids
