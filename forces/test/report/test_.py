# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from forces.model import (
    ForcesConfig,
    KindEnum,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityType,
)
from forces.report import (
    generate_raw_report,
    get_summary_template,
    style_report,
    style_summary,
)
from forces.report.filters import (
    filter_repo,
)
from forces.report.formatters import (
    create_findings_dict,
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
        for key in ("open", "closed", "accepted"):
            assert key in find

    findings_dict_2 = await create_findings_dict(
        group=test_group, api_token=test_token
    )
    for find in findings_dict_2.values():
        for key in ("open", "closed", "accepted"):
            assert key in find


@pytest.mark.asyncio
async def test_generate_report1(
    test_group: str,
    test_token: str,
    test_finding: str,
) -> None:
    config = ForcesConfig(group=test_group)
    report = await generate_raw_report(
        config=config,
        api_token=test_token,
    )
    assert report["summary"]["total"] == 9
    assert report["summary"]["open"]["total"] == 7
    assert report["summary"]["closed"]["total"] == 2

    findings = [
        find for find in report["findings"] if find["id"] == test_finding
    ]
    assert len(findings) == 1


@pytest.mark.asyncio
async def test_generate_report2(
    test_group: str,
    test_token: str,
    test_finding: str,
) -> None:
    config = ForcesConfig(group=test_group)
    report = await generate_raw_report(
        config=config,
        api_token=test_token,
    )
    findings = [
        find for find in report["findings"] if find["id"] == test_finding
    ]
    assert len(findings[0]["vulnerabilities"]) == 5


def test_get_summary_template() -> None:
    assert get_summary_template(KindEnum.ALL) == {
        "open": {"DAST": 0, "SAST": 0, "total": 0},
        "closed": {"DAST": 0, "SAST": 0, "total": 0},
        "accepted": {"DAST": 0, "SAST": 0, "total": 0},
    }
    assert get_summary_template(KindEnum.DYNAMIC) == {
        "open": {"total": 0},
        "closed": {"total": 0},
        "accepted": {"total": 0},
    }


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
        url="https://app.fluidattacks.com/groups/testGroup/vulns/111",
        state=VulnerabilityState.OPEN,
        severity=6.0,
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
