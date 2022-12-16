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
            "date": "2018-04-07 19:45:15",
            "source": "asm",
            "state": "APPROVED",
        },
    ]
    release_date: str = "2018-04-07 19:45:15"
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
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    title: str = "001. SQL injection - C Sharp SQL API"
    description: str = "I just have updated the description"
    requirements: str = (
        "REQ.0132. Passwords (phrase type) must be at least 3 words long."
    )
    attack_vector_description: str = "This is an updated attack vector"
    min_time_to_remediate: int = 4
    threat: str = "Updated threat"
    recommendation: str = "Updated recommendation"
    tracking: List[Dict[str, Any]] = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "date": "2018-04-08",
            "accepted": 0,
            "acceptedUndefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 1,
            "open": 0,
            "closed": 1,
            "date": "2018-04-08",
            "accepted": 0,
            "acceptedUndefined": 0,
            "assigned": "",
            "justification": "",
        },
        {
            "cycle": 2,
            "open": 0,
            "closed": 0,
            "date": "2018-04-09",
            "accepted": 1,
            "acceptedUndefined": 0,
            "assigned": "anything@gmail.com",
            "justification": "justification",
        },
    ]
    treatment_summary: Dict[str, int] = {
        "accepted": 1,
        "acceptedUndefined": 2,
        "inProgress": 3,
        "new": 4,
    }
    verification_summary: Dict[str, int] = {
        "requested": 1,
        "onHold": 2,
        "verified": 3,
    }
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    where: str = "192.168.1.2"
    assert "errors" not in result
    assert result["data"]["finding"]["age"] == age
    assert result["data"]["finding"]["hacker"] == hacker
    assert (
        result["data"]["finding"]["attackVectorDescription"]
        == attack_vector_description
    )
    assert result["data"]["finding"]["closedVulnerabilities"] == 3
    assert result["data"]["finding"]["consulting"] == [
        {
            "content": (
                "Regarding vulnerabilities: \n"
                "  - 192.168.1.20\n\n"
                "This is a test observations"
            ),
            "created": "2019/05/28 15:09:37",
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
    assert result["data"]["finding"]["isExploitable"] == is_exploitable
    assert result["data"]["finding"]["lastVulnerability"] == last_vuln
    assert result["data"]["finding"]["observations"] == [
        {"content": "This is a test observations"}
    ]
    assert result["data"]["finding"]["openAge"] == open_age
    assert result["data"]["finding"]["openVulnerabilities"] == 5
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
    assert (
        result["data"]["finding"]["verificationSummary"]
        == verification_summary
    )
    assert result["data"]["finding"]["verified"] == verified
    assert (
        result["data"]["finding"]["minTimeToRemediate"]
        == min_time_to_remediate
    )
    assert result["data"]["finding"]["where"] == where
    assert result["data"]["finding"]["vulnerabilitiesConnection"] == {
        "edges": [
            {
                "node": {"id": "be09edb7-cd5c-47ed-bee4-97c645acdce8"},
            },
            {
                "node": {"id": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a"},
            },
        ],
        "pageInfo": {
            "endCursor": (
                "eyJwayI6ICJWVUxOIzY0MDFiYzg3LTg2MzMtNGE0YS04ZDhlLTdk"
                "YWUwY2E1N2U2YSIsICJzayI6ICJGSU4jM2M0NzUzODQtODM0Yy00N2IwLWFjN"
                "zEtYTQxYTAyMmU0MDFjIiwgInBrXzUiOiAiRklOIzNjNDc1Mzg0LTgzNGMtND"
                "diMC1hYzcxLWE0MWEwMjJlNDAxYyIsICJza181IjogIlZVTE4jREVMRVRFRCN"
                "mYWxzZSNaUiNmYWxzZSNTVEFURSNvcGVuI1ZFUklGI25vbmUifQ=="
            ),
            "hasNextPage": False,
        },
    }
    assert result["data"]["finding"][
        "vulnerabilitiesToReattackConnection"
    ] == {
        "edges": [],
        "pageInfo": {"endCursor": "bnVsbA==", "hasNextPage": False},
    }
    assert result["data"]["finding"]["zeroRiskConnection"] == {
        "edges": [
            {
                "node": {"id": "7771bc87-8633-4a4a-8d8e-7dae0ca57e7a"},
            }
        ],
        "pageInfo": {
            "endCursor": (
                "eyJwayI6ICJWVUxOIzc3NzFiYzg3LTg2MzMtNGE0YS04ZDhlLTdk"
                "YWUwY2E1N2U3YSIsICJzayI6ICJGSU4jM2M0NzUzODQtODM0Yy00N2IwLWFjN"
                "zEtYTQxYTAyMmU0MDFjIiwgInBrXzUiOiAiRklOIzNjNDc1Mzg0LTgzNGMtND"
                "diMC1hYzcxLWE0MWEwMjJlNDAxYyIsICJza181IjogIlZVTE4jREVMRVRFRCN"
                "mYWxzZSNaUiN0cnVlI1NUQVRFI29wZW4jVkVSSUYjbm9uZSJ9"
            ),
            "hasNextPage": False,
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("finding")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@fluidattacks.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
@freeze_time("2021-03-31")
async def test_get_finding_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
