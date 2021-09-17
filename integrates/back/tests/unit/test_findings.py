from back.tests.unit import (
    MIGRATION,
)
from collections import (
    OrderedDict,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    FindingVerification,
)
from findings.dal import (
    get_finding,
)
from findings.domain import (
    download_evidence_file,
    get_records_from_file,
)
from newutils.findings import (
    format_data,
    get_evidence,
)
from newutils.vulnerabilities import (
    get_reattack_requesters,
    get_reattack_requesters_new,
)
import os
import pytest
from typing import (
    Tuple,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
async def test_get_evidence() -> None:
    finding = await get_finding("422286126")
    name = "test_name"
    item = [
        {"description": "desc", "file_url": "test.png", "name": "test_name"},
        {
            "description": "des2",
            "file_url": "test2.png",
            "name": "test_name_2",
        },
    ]

    test_data = get_evidence(name, item, finding)
    expected_output = {
        "description": "desc",
        "date": "2018-07-09 00:00:00",
        "url": "test.png",
    }
    assert test_data == expected_output

    name = "non-existing name"
    test_data = get_evidence(name, item, finding)
    expected_output = {"url": "", "description": ""}
    assert test_data == expected_output


async def test_download_evidence_file() -> None:
    group_name = "unittesting"
    finding_id = "422286126"
    file_name = "unittesting-422286126-evidence_route_1.png"
    test_data = await download_evidence_file(group_name, finding_id, file_name)
    expected_output = os.path.abspath(
        # FP: local testing
        "/tmp/unittesting-422286126-evidence_route_1.png"  # NOSONAR
    )
    assert test_data == expected_output


async def test_get_records_from_file() -> None:
    group_name = "unittesting"
    finding_id = "422286126"
    file_name = "unittesting-422286126-evidence_file.csv"
    test_data = await get_records_from_file(group_name, finding_id, file_name)
    expected_output = [
        OrderedDict(
            [
                ("song", "a million little pieces"),
                ("artist", "placebo"),
                ("year", "2010"),
            ]
        ),
        OrderedDict(
            [
                ("song", "heart shaped box"),
                ("artist", "nirvana"),
                ("year", "1992"),
            ]
        ),
        OrderedDict(
            [("song", "zenith"), ("artist", "ghost"), ("year", "2015")]
        ),
        OrderedDict(
            [("song", "hysteria"), ("artist", "def leppard"), ("year", "1987")]
        ),
    ]

    assert test_data == expected_output


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
async def test_format_data() -> None:
    finding_id = "422286126"
    finding_to_test = await get_finding(finding_id)
    test_data = list(format_data(finding_to_test).keys())
    expected_keys = [
        "context",
        "modifiedSeverityScope",
        "availabilityRequirement",
        "evidence",
        "availabilityImpact",
        "modifiedPrivilegesRequired",
        "modifiedAttackVector",
        "testType",
        "id",
        "affectedSystems",
        "attackVectorDesc",
        "requirements",
        "severity",
        "cvssBasescore",
        "userInteraction",
        "cvssEnv",
        "privilegesRequired",
        "interested",
        "projectName",
        "groupName",
        "finding",
        "confidentialityImpact",
        "integrityRequirement",
        "remediationLevel",
        "leader",
        "modifiedConfidentialityImpact",
        "files",
        "modifiedUserInteraction",
        "attackComplexity",
        "attackVector",
        "reportConfidence",
        "cvssTemporal",
        "remediated",
        "clientProject",
        "compromisedAttrs",
        "findingType",
        "historicState",
        "exploitable",
        "confidentialityRequirement",
        "records",
        "recordsNumber",
        "modifiedAttackComplexity",
        "severityScope",
        "cvssVersion",
        "analyst",
        "subscription",
        "effectSolution",
        "reportLevel",
        "severityCvss",
        "modifiedAvailabilityImpact",
        "vulnerability",
        "findingId",
        "threat",
        "integrityImpact",
        "modifiedIntegrityImpact",
        "relatedFindings",
        "exploitability",
    ]

    assert sorted(test_data) == sorted(expected_keys)


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
async def test_get_reattack_requesters() -> None:
    finding = await get_finding("463558592")
    recipients = get_reattack_requesters(
        finding.get("historic_verification", []),
        ["3bcdb384-5547-4170-a0b6-3b397a245465"],
    )
    assert recipients == ["integratesuser@gmail.com"]


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
async def test_get_reattack_requesters_new() -> None:
    loaders = get_new_context()
    historic_verification: Tuple[
        FindingVerification, ...
    ] = await loaders.finding_historic_verification_new.load("463558592")
    recipients = get_reattack_requesters_new(
        historic_verification,
        {"3bcdb384-5547-4170-a0b6-3b397a245465"},
    )
    assert recipients == ["integratesuser@gmail.com"]
