from decimal import (
    Decimal,
)
from forces.model import (
    Finding,
    ForcesConfig,
    KindEnum,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityType,
)
from forces.report import (
    generate_raw_report,
)
from forces.report.filters import (
    filter_repo,
)
from forces.report.formatters import (
    create_findings_dict,
)
from forces.report.styles import (
    style_report,
    style_summary,
)
import pytest


@pytest.mark.asyncio
async def test_create_findings_dict(
    test_group: str,
    test_token: str,
) -> None:
    findings_dict_1 = await create_findings_dict(
        group=test_group, api_token=test_token
    )
    for find in findings_dict_1.values():
        assert find.identifier
        assert find.title
        assert find.state
        assert find.exploitability


@pytest.mark.asyncio
async def test_generate_report(
    test_group: str,
    test_token: str,
    test_finding: str,
) -> None:
    config = ForcesConfig(group=test_group)
    report = await generate_raw_report(
        config=config,
        api_token=test_token,
    )
    find: Finding = next(
        find for find in report.findings if find.identifier == test_finding
    )
    assert len(find.vulnerabilities) == 5

    identifiers: set[str] = {find.identifier for find in report.findings}
    assert len(identifiers) == len(report.findings)

    assert report.summary.open.total == 7
    assert report.summary.closed.total == 2
    assert report.summary.accepted.total == 0
    assert (
        report.summary.total
        == sum([len(finding.vulnerabilities) for finding in report.findings])
        == 9
    )


def test_style_summary() -> None:
    assert style_summary(VulnerabilityState.ACCEPTED, 1) == "1"
    assert style_summary(VulnerabilityState.OPEN, 0) == "[green]0[/]"
    assert style_summary(VulnerabilityState.OPEN, 9) == "[yellow3]9[/]"
    assert style_summary(VulnerabilityState.OPEN, 17) == "[orange3]17[/]"
    assert style_summary(VulnerabilityState.OPEN, 25) == "[red]25[/]"
    assert style_summary(VulnerabilityState.CLOSED, 15) == "[green]15[/]"


def test_style_report() -> None:
    assert style_report("tittle", "some_value") == "some_value"
    assert style_report("title", "some_value") == "[yellow]some_value[/]"
    assert style_report("state", "open") == "[red]open[/]"
    assert style_report("state", "openn") == "openn"


def test_filter_repo() -> None:
    vuln: Vulnerability = Vulnerability(
        type=VulnerabilityType.DAST,
        where="somewhere",
        specific="port 21",
        state=VulnerabilityState.OPEN,
        severity=Decimal("6.0"),
        report_date="",
        exploitability=4.5,
        root_nickname=None,
    )
    assert filter_repo(
        vuln=vuln,
        repo_name="root_test",
        kind=KindEnum.DYNAMIC,
    )
    assert filter_repo(
        vuln=vuln,
        kind=KindEnum.DYNAMIC,
    )
