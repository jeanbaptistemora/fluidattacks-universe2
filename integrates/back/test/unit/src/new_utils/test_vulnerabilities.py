from custom_exceptions import (
    InvalidRange,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.roots.types import (
    RootRequest,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
)
from newutils.vulnerabilities import (
    as_range,
    format_vulnerabilities,
    get_closing_date,
    get_opening_date,
    get_ranges,
    get_treatment_from_org_finding_policy,
    group_specific,
    is_range,
    is_sequence,
    range_to_list,
    sort_vulnerabilities,
    ungroup_specific,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


def test_as_range() -> None:
    range_to_stringify = [1, 2, 3, 4, 5]
    test_data = as_range(range_to_stringify)
    expected_output = "1-5"
    assert test_data == expected_output


async def test_format_vulnerabilities() -> None:
    loaders: Dataloaders = get_new_context()
    finding_id = "422286126"
    group_name: str = "unittesting"
    finding_vulns = await loaders.finding_vulnerabilities.load(finding_id)
    vulns_roots = await loaders.root.load_many(
        [
            RootRequest(group_name=group_name, root_id=vuln.root_id or "")
            for vuln in finding_vulns
        ]
    )
    test_data = format_vulnerabilities(finding_vulns, vulns_roots)
    expected_output = {
        "inputs": [
            {
                "url": "https://example.com",
                "field": "phone",
                "state": "open",
                "source": "analyst",
                "tool": {"impact": "indirect", "name": "tool-2"},
            }
        ],
        "lines": [
            {
                "commit_hash": "ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                "line": "12",
                "path": "test/data/lib_path/f060/csharp.cs",
                "state": "open",
                "source": "analyst",
                "tool": {"impact": "indirect", "name": "tool-2"},
            }
        ],
        "ports": [],
    }
    assert test_data == expected_output


async def test_get_vuln_closing_date() -> None:
    closed_vulnerability = Vulnerability(
        created_by="test@test.com",
        created_date=datetime.fromisoformat("2019-01-08T21:01:26+00:00"),
        finding_id="422286126",
        group_name="unittesting",
        hacker_email="test@test.com",
        id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
        state=VulnerabilityState(
            modified_by="test@test.com",
            modified_date=datetime.fromisoformat("2019-01-08T21:01:26+00:00"),
            source=Source.ASM,
            specific="phone",
            status=VulnerabilityStateStatus.SAFE,
            where="https://example.com",
        ),
        type=VulnerabilityType.INPUTS,
        unreliable_indicators=VulnerabilityUnreliableIndicators(
            unreliable_source=Source.ASM,
        ),
    )
    test_data = get_closing_date(closed_vulnerability)
    closing_date = datetime(2019, 1, 8).date()
    assert test_data == closing_date

    loaders = get_new_context()
    open_vulnerability = await loaders.vulnerability.load(
        "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    )
    assert open_vulnerability
    test_data = get_closing_date(open_vulnerability)
    assert test_data is None


async def test_get_vuln_opening_date() -> None:
    test_vuln = Vulnerability(
        created_by="test@test.com",
        created_date=datetime.fromisoformat("2019-01-08T21:01:26+00:00"),
        finding_id="",
        group_name="",
        hacker_email="",
        id="",
        type=VulnerabilityType.LINES,
        state=VulnerabilityState(
            modified_by="",
            modified_date=datetime.fromisoformat("2019-01-08T21:01:26+00:00"),
            source=Source.ASM,
            specific="",
            status=VulnerabilityStateStatus.VULNERABLE,
            where="",
        ),
        unreliable_indicators=VulnerabilityUnreliableIndicators(
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
        ),
    )
    result_date = get_opening_date(test_vuln)
    assert result_date == datetime(2019, 1, 8).date()

    min_date = datetime(2021, 1, 1).date()
    result_date = get_opening_date(vuln=test_vuln, min_date=min_date)
    assert result_date is None

    loaders = get_new_context()
    test_open_vuln = await loaders.vulnerability.load(
        "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    )
    assert test_open_vuln
    result_date = get_opening_date(test_open_vuln)
    expected_output = datetime(2020, 9, 9).date()
    assert result_date == expected_output


def test_get_ranges() -> None:
    working_list = [1, 2, 3, 7, 9, 10, 11, 12, 13, 19]
    test_data = get_ranges(working_list)
    expected_output = "1-3,7,9-13,19"
    assert test_data == expected_output


@pytest.mark.parametrize(
    ["modified_date", "user_email"],
    [
        [
            datetime.fromisoformat("2020-01-01T20:07:57+00:00"),
            "unittesting@fluidattacks.com",
        ]
    ],
)
def test_get_treatment_from_org_finding_policy(
    modified_date: datetime, user_email: str
) -> None:
    result = get_treatment_from_org_finding_policy(
        modified_date=modified_date, user_email=user_email
    )
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(
        isinstance(result[i], VulnerabilityTreatment)
        for i in range(len(result))
    )


async def test_group_specific() -> None:
    loaders = get_new_context()
    vulns = await loaders.finding_vulnerabilities_all.load("422286126")
    test_data = group_specific(vulns, VulnerabilityType.INPUTS)
    assert isinstance(test_data, list)
    assert len(test_data) == 2
    assert isinstance(test_data[0], Vulnerability)
    assert test_data[0] is not None


def test_is_range() -> None:
    range_value = "100-200"
    no_range_value = "20"
    assert is_range(range_value)
    assert not is_range(no_range_value)


def test_is_sequence() -> None:
    secuence_value = "20,21,22"
    no_secuence_values = ["20-30", "20"]
    assert is_sequence(secuence_value)
    for no_secuence_value in no_secuence_values:
        assert not is_sequence(no_secuence_value)


@pytest.mark.parametrize(
    ["range_value", "expected_output", "range_to_raise_exception"],
    [["10-15", ["10", "11", "12", "13", "14", "15"], "13-12"]],
)
def test_range_to_list(
    range_value: str,
    expected_output: list,
    range_to_raise_exception: str,
) -> None:
    result = range_to_list(range_value)
    assert isinstance(result, list)
    assert result == expected_output
    with pytest.raises(InvalidRange):
        assert range_to_list(range_to_raise_exception)


def test_sort_vulnerabilities() -> None:
    vulns = [
        Vulnerability(
            created_by="test@test.com",
            created_date=datetime.fromisoformat("2018-04-08T00:45:11+00:00"),
            finding_id="",
            group_name="",
            hacker_email="",
            id="",
            state=VulnerabilityState(
                modified_by="",
                modified_date=datetime.fromisoformat(
                    "2019-01-08T21:01:26+00:00"
                ),
                source=Source.ASM,
                specific="",
                status=VulnerabilityStateStatus.VULNERABLE,
                where=where,
            ),
            type=VulnerabilityType.INPUTS,
            unreliable_indicators=VulnerabilityUnreliableIndicators(
                unreliable_source=Source.ASM,
            ),
        )
        for where in ("abaa", "1abc", "aaaa")
    ]
    expected_output = [
        Vulnerability(
            created_by="test@test.com",
            created_date=datetime.fromisoformat("2018-04-08T00:45:11+00:00"),
            finding_id="",
            group_name="",
            hacker_email="",
            id="",
            state=VulnerabilityState(
                modified_by="",
                modified_date=datetime.fromisoformat(
                    "2019-01-08T21:01:26+00:00"
                ),
                source=Source.ASM,
                specific="",
                status=VulnerabilityStateStatus.VULNERABLE,
                where=where,
            ),
            type=VulnerabilityType.INPUTS,
            unreliable_indicators=VulnerabilityUnreliableIndicators(
                unreliable_source=Source.ASM,
            ),
        )
        for where in ("1abc", "aaaa", "abaa")
    ]
    test_data = sort_vulnerabilities(vulns)
    assert test_data == expected_output


def test_ungroup_specific() -> None:
    specific = "13,14,18-20,24-30,40"
    test_data = ungroup_specific(specific)
    expected_output = [
        "13",
        "14",
        "18",
        "19",
        "20",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "40",
    ]
    assert isinstance(test_data, list)
    assert test_data == expected_output
