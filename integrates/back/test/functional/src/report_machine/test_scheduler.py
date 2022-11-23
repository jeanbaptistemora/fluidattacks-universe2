from custom_exceptions import (
    InvalidRootComponent,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
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
from finding_comments import (
    domain as comments_domain,
)
import json
import pytest
from server.report_machine import (
    process_execution,
)
from typing import (
    Optional,
    Tuple,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine_s3")
async def test_persist_result(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/persist_result.sarif",
        "rb",
    ) as sarif:
        sarif_report = json.load(sarif)

    with mock.patch(
        "server.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "nickname",
                "language": "EN",
                "path": {"include": ["back/src/"], "exclude": []},
                "apk": {"include": [], "exclude": []},
            }
        ),
    ):
        with mock.patch(
            "server.report_machine.get_sarif_log",
            side_effect=mock.AsyncMock(return_value=sarif_report),
        ):
            await process_execution("group1_1234345")

            loaders = get_new_context()
            group_findings: Tuple[
                Finding, ...
            ] = await loaders.group_drafts_and_findings.load("group1")
            finding_001: Optional[Finding] = next(
                (
                    finding
                    for finding in group_findings
                    if "001" in finding.title
                ),
                None,
            )
            assert finding_001 is not None

            integrates_vulnerabilities: Tuple[Vulnerability, ...] = tuple(
                vuln
                for vuln in await loaders.finding_vulnerabilities.load(
                    finding_001.id
                )
                if vuln.state.status == VulnerabilityStateStatus.OPEN
                and vuln.state.source == Source.MACHINE
                and vuln.root_id == "88637616-41d4-4242-854a-db8ff7fe1ab6"
            )
            # The execution must close vulnerabilities in the scope
            closed_vuln = await loaders.vulnerability.load(
                "4dbc01e0-4cfc-4b77-9b71-bb7566c60bg"
            )
            closed_vuln_historic = (
                await loaders.vulnerability_historic_state.load(
                    "4dbc01e0-4cfc-4b77-9b71-bb7566c60bg"
                )
            )
            assert len(integrates_vulnerabilities) == 3
            assert closed_vuln.state.status == VulnerabilityStateStatus.CLOSED
            assert (
                closed_vuln_historic[-1].commit
                == "7fd232de194916018c4ba68f5cb6dc595e99df7e"
            )
            assert finding_001.evidences.evidence5 is not None
            assert finding_001.evidences.evidence1 is None
            assert (
                "sql injection in"
                in finding_001.evidences.evidence5.description
            )

            comments = await comments_domain.get_comments(
                loaders=loaders,
                group_name="group1",
                finding_id=finding_001.id,
                user_email="machine@fludidattacks.com",
            )
            assert len(comments) == 1

            for comment in comments:
                if "still open" in comment.content:
                    assert "back/src/index.js" in comment.content
                elif "were solved" in comment.content:
                    assert (
                        "back/src/controller/user/index.js" in comment.content
                    )
                    assert "back/src/model/user/index.js" in comment.content


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine_s3")
async def test_report_f079(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/report_f079.sarif", "rb"
    ) as sarif:
        sarif_report = json.load(sarif)

    with mock.patch(
        "server.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "nickname",
                "language": "EN",
                "path": {
                    "include": [
                        "skims/test/data/lib_path/f011/requirements.txt"
                    ],
                    "exclude": [],
                },
                "apk": {"include": [], "exclude": []},
            }
        ),
    ):
        with mock.patch(
            "server.report_machine.get_sarif_log",
            side_effect=mock.AsyncMock(return_value=sarif_report),
        ):
            loaders = get_new_context()
            group_findings: Tuple[
                Finding, ...
            ] = await loaders.group_drafts_and_findings.load("group1")
            finding_f079: Optional[Finding] = next(
                (
                    finding
                    for finding in group_findings
                    if finding.title.startswith("079")
                ),
                None,
            )
            assert finding_f079 is None

            await process_execution("group1_1234345")

            loaders.group_drafts_and_findings.clear("group1")
            group_findings = await loaders.group_drafts_and_findings.load(
                "group1"
            )
            finding_f079 = next(
                (
                    finding
                    for finding in group_findings
                    if finding.title.startswith("079")
                ),
                None,
            )
            assert finding_f079 is not None
            assert finding_f079.submission is not None
            assert finding_f079.approval is not None
            assert (
                finding_f079.submission.status == FindingStateStatus.SUBMITTED
            )
            assert finding_f079.approval.status == FindingStateStatus.APPROVED
            assert (
                finding_f079.submission.modified_date
                != finding_f079.approval.modified_date
            )

            integrates_vulnerabilities: Tuple[Vulnerability, ...] = tuple(
                vuln
                for vuln in await loaders.finding_vulnerabilities.load(
                    finding_f079.id
                )
                if vuln.state.status == VulnerabilityStateStatus.OPEN
                and vuln.state.source == Source.MACHINE
            )

            assert len(integrates_vulnerabilities) == 1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine_s3")
async def test_duplicated_reports(populate: bool) -> None:
    assert populate
    with open(
        (
            "back/test/functional/src/report_machine/sarif/"
            "duplicated_report_1.sarif"
        ),
        "rb",
    ) as sarif_1:
        with open(
            (
                "back/test/functional/src/report_machine/sarif/"
                "duplicated_report_2.sarif"
            ),
            "rb",
        ) as sarif_2:
            sarif_report_1 = json.load(sarif_1)
            sarif_report_2 = json.load(sarif_2)

    with mock.patch(
        "server.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "nickname",
                "language": "EN",
                "path": {
                    "include": ["skims/test/data/lib_path/f011/build.gradle"],
                    "exclude": [],
                },
                "apk": {"include": [], "exclude": []},
            },
        ),
    ), mock.patch(
        "server.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(
            side_effect=[sarif_report_1, sarif_report_2],
        ),
    ):
        await process_execution("group1_1234345")

        loaders = get_new_context()
        group_findings: Tuple[
            Finding, ...
        ] = await loaders.group_drafts_and_findings.load("group1")
        finding_011: Optional[Finding] = next(
            (finding for finding in group_findings if "011" in finding.title),
            None,
        )
        assert finding_011 is not None

        integrates_vulnerabilities: Tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(
                finding_011.id
            )
            if vuln.state.status == VulnerabilityStateStatus.OPEN
            and vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities) == 1

        where_1 = integrates_vulnerabilities[0].state.where
        await process_execution("group1_4d3275db-5715-4258-a2d5-dc80c441b062")
        loaders.finding_vulnerabilities.clear(finding_011.id)
        integrates_vulnerabilities_2: Tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(
                finding_011.id
            )
            if vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities_2) == 1

        where_2 = integrates_vulnerabilities_2[0].state.where
        assert where_1 == where_2


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine_s3")
async def test_approval(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/approval.sarif",
        "rb",
    ) as sarif:
        sarif_report = json.load(sarif)

    with mock.patch(
        "server.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "nickname",
                "language": "EN",
                "path": {"include": ["."], "exclude": []},
                "apk": {"include": [], "exclude": []},
            },
        ),
    ), mock.patch(
        "server.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(return_value=sarif_report),
    ):
        loaders = get_new_context()
        findings: Tuple[
            Finding, ...
        ] = await loaders.group_drafts_and_findings.load("group1")
        f_117: Optional[Finding] = next(
            (fin for fin in findings if fin.title.startswith("117")), None
        )
        f_237: Optional[Finding] = next(
            (fin for fin in findings if fin.title.startswith("237")), None
        )
        assert f_117 is not None
        assert f_237 is None

        f_117_vulns: Tuple[
            Vulnerability, ...
        ] = await loaders.finding_vulnerabilities.load(f_117.id)
        assert len(f_117_vulns) == 1
        assert (f_117_vulns[0].state.where, f_117_vulns[0].state.specific) == (
            ".project",
            "0",
        )

        await process_execution("group1_")
        loaders.group_drafts_and_findings.clear("group1")
        loaders.finding_vulnerabilities.clear(f_117.id)

        findings = await loaders.group_drafts_and_findings.load("group1")
        f_117 = next(
            (fin for fin in findings if fin.title.startswith("117")), None
        )
        f_237 = next(
            (fin for fin in findings if fin.title.startswith("237")), None
        )
        assert f_117 is not None
        assert f_237 is not None

        f_117_vulns = await loaders.finding_vulnerabilities.load(f_117.id)
        f_237_vulns: Tuple[
            Vulnerability, ...
        ] = await loaders.finding_vulnerabilities.load(f_237.id)
        assert len(f_117_vulns) == 3
        assert len(f_237_vulns) == 3

        assert f_117.approval is None
        assert f_237.approval is not None
        assert f_237.approval.status == FindingStateStatus.APPROVED
        assert f_237.approval.source == Source.MACHINE


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine_s3")
async def test_report_inputs(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/report_inputs.sarif",
        "rb",
    ) as sarif:
        sarif_report = json.load(sarif)
    with open(
        "back/test/functional/src/report_machine/sarif/"
        "invalid_component.sarif",
        "rb",
    ) as sarif:
        invalid_sarif_report = json.load(sarif)

    with mock.patch(
        "server.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "nickname",
                "language": "EN",
                "dast": {"http": {"include": ["http://localhost:48000/"]}},
                "path": {"include": [], "exclude": []},
                "apk": {"include": [], "exclude": []},
            },
        ),
    ), mock.patch(
        "server.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(
            side_effect=[sarif_report, invalid_sarif_report]
        ),
    ):
        loaders = get_new_context()
        findings: Tuple[
            Finding, ...
        ] = await loaders.group_drafts_and_findings.load("group1")
        f_128: Optional[Finding] = next(
            (fin for fin in findings if fin.title.startswith("128")), None
        )
        assert f_128 is None

        await process_execution("group1_")
        loaders.group_drafts_and_findings.clear("group1")

        findings = await loaders.group_drafts_and_findings.load("group1")
        f_128 = next(
            (fin for fin in findings if fin.title.startswith("128")), None
        )
        assert f_128 is not None
        assert f_128.submission is not None
        assert f_128.submission.status == FindingStateStatus.SUBMITTED
        assert f_128.submission.source == Source.MACHINE
        assert f_128.approval is None

        f_128_vulns = await loaders.finding_vulnerabilities.load(f_128.id)
        assert len(f_128_vulns) == 3

        with pytest.raises(InvalidRootComponent):
            await process_execution("group1_")
