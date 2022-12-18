from collections import (
    OrderedDict,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_severity_score,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
from schedulers.update_indicators import (
    create_data_format_chart,
    create_register_by_week,
    create_weekly_date,
    get_accepted_vulns,
    get_by_time_range,
    get_date_last_vulns,
    get_first_week_dates,
    get_status_vulns_by_time_range,
)
from typing import (
    Any,
)
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_create_data_format_chart() -> None:
    registers = OrderedDict(
        [
            (
                "Sep 24 - 30, 2018",  # NOSONAR
                {
                    "found": 2,
                    "accepted": 0,
                    "closed": 0,
                    "assumed_closed": 0,
                    "opened": 2,
                },
            )
        ]
    )
    test_data = create_data_format_chart(registers)  # type: ignore
    expected_output = [
        [{"y": 2, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 2, "x": "Sep 24 - 30, 2018"}],
    ]
    assert test_data == expected_output


def test_create_weekly_date() -> None:
    first_date = datetime.fromisoformat("2019-09-19T13:23:32-05:00")
    test_data = create_weekly_date(first_date)
    expected_output = "Sep 16 - 22, 2019"
    assert test_data == expected_output


async def test_create_register_by_week(
    dynamo_resource: ServiceResource,
) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders = get_new_context()
    group_name = "unittesting"
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        test_data = await create_register_by_week(loaders, group_name)
    assert isinstance(test_data.vulnerabilities, list)
    for item in test_data.vulnerabilities:
        assert isinstance(item, list)
        assert isinstance(item[0], dict)
        assert item[0] is not None


async def test_get_accepted_vulns(dynamo_resource: ServiceResource) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders = get_new_context()
    last_day = datetime.fromisoformat("2019-06-30T23:59:59-05:00")
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        findings: tuple[Finding, ...] = await loaders.group_findings.load(
            "unittesting"
        )
        vulnerabilities = (
            await loaders.finding_vulnerabilities_nzr.load_many_chained(
                [finding.id for finding in findings]
            )
        )
        findings_severity: dict[str, Decimal] = {
            finding.id: get_severity_score(finding.severity)
            for finding in findings
        }
        vulnerabilities_severity = [
            findings_severity[vulnerability.finding_id]
            for vulnerability in vulnerabilities
        ]
        historic_states = await loaders.vulnerability_historic_state.load_many(
            [vuln.id for vuln in vulnerabilities]
        )
        historic_treatments = (
            await loaders.vulnerability_historic_treatment.load_many(
                [vuln.id for vuln in vulnerabilities]
            )
        )
    test_data = sum(
        [
            get_accepted_vulns(
                historic_state, historic_treatment, severity, last_day
            ).vulnerabilities
            for historic_state, historic_treatment, severity in zip(
                historic_states,
                historic_treatments,
                vulnerabilities_severity,
            )
        ]
    )
    expected_output = 1
    assert test_data == expected_output


async def test_get_by_time_range(dynamo_resource: ServiceResource) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders = get_new_context()
    last_day = datetime.fromisoformat("2020-09-09T23:59:59-05:00")
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        vulnerability: Vulnerability = await loaders.vulnerability.load(
            "15375781-31f2-4953-ac77-f31134225747"
        )
        finding: Finding = await loaders.finding.load(vulnerability.finding_id)

        historic_state = await loaders.vulnerability_historic_state.load(
            vulnerability.id
        )
    assert mock_table_resource.called is True
    vulnerability_severity = get_severity_score(finding.severity)
    test_data = get_by_time_range(
        historic_state,
        VulnerabilityStateStatus.OPEN,
        vulnerability_severity,
        last_day,
    )
    expected_output = (1, Decimal("0.144"))
    assert test_data == expected_output


async def test_get_date_last_vulns(dynamo_resource: ServiceResource) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders: Dataloaders = get_new_context()
    finding_id = "422286126"
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        vulns = await loaders.finding_vulnerabilities.load(finding_id)
    test_data = get_date_last_vulns(vulns)
    expected_output = datetime.fromisoformat("2019-12-30T17:46:10+00:00")
    assert mock_table_resource.called is True
    assert test_data == expected_output


async def test_get_first_week_dates(dynamo_resource: ServiceResource) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders: Dataloaders = get_new_context()
    finding_id = "422286126"
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        vulns = await loaders.finding_vulnerabilities.load(finding_id)
    test_data = get_first_week_dates(vulns)
    expected_output = (
        datetime.fromisoformat("2019-12-30T00:00:00+00:00"),
        datetime.fromisoformat("2020-01-05T23:59:59+00:00"),
    )
    assert mock_table_resource.called is True
    assert test_data == expected_output


async def test_get_status_vulns_by_time_range(
    # pylint: disable=too-many-locals
    dynamo_resource: ServiceResource,
) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    first_day = datetime.fromisoformat("2019-06-01T12:00:00+00:00")
    last_day = datetime.fromisoformat("2020-02-28T23:59:59+00:00")
    loaders = get_new_context()
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        findings: tuple[Finding, ...] = await loaders.group_findings.load(
            "unittesting"
        )
        vulnerabilities = (
            await loaders.finding_vulnerabilities_nzr.load_many_chained(
                [finding.id for finding in findings]
            )
        )
        findings_severity: dict[str, Decimal] = {
            finding.id: get_severity_score(finding.severity)
            for finding in findings
        }
        vulnerabilities_severity = [
            findings_severity[vulnerabilities.finding_id]
            for vulnerabilities in vulnerabilities
        ]
        historic_states = await loaders.vulnerability_historic_state.load_many(
            [vulnerabilities.id for vulnerabilities in vulnerabilities]
        )
        historic_treatments = (
            await loaders.vulnerability_historic_treatment.load_many(
                [vulnerabilities.id for vulnerabilities in vulnerabilities]
            )
        )
    assert mock_table_resource.called is True
    test_data = get_status_vulns_by_time_range(
        vulnerabilities=vulnerabilities,
        vulnerabilities_severity=vulnerabilities_severity,
        vulnerabilities_historic_states=historic_states,
        vulnerabilities_historic_treatments=historic_treatments,
        first_day=first_day,
        last_day=last_day,
    )

    expected_output = {"found": 2, "accepted": 1, "closed": 0, "opened": 2}
    output = {
        "found": test_data.found_vulnerabilities,
        "accepted": test_data.accepted_vulnerabilities,
        "closed": test_data.closed_vulnerabilities,
        "opened": test_data.open_vulnerabilities,
    }
    expected_output_cvssf = {
        "found": Decimal("0.362"),
        "accepted": Decimal("24.251"),
        "closed": Decimal("0"),
        "opened": Decimal("0.362"),
    }
    output_cvssf = {
        "found": test_data.found_cvssf,
        "accepted": test_data.accepted_cvssf,
        "closed": test_data.closed_cvssf,
        "opened": test_data.open_cvssf,
    }
    assert sorted(output.items()) == sorted(expected_output.items())
    assert sorted(output_cvssf.items()) == sorted(
        expected_output_cvssf.items()
    )
