# pylint: disable=import-outside-toplevel
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Source,
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
from newutils.findings import (
    get_requirements_file,
    get_vulns_file,
)
import pytest
from typing import (
    Tuple,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_persist_result(populate: bool) -> None:
    assert populate
    criteria_vulns = await get_vulns_file()
    criteria_reqs = get_requirements_file()
    with mock.patch(
        "schedulers.report_machine.get_config",
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
            "schedulers.report_machine.get_sarif_log",
            side_effect=mock.AsyncMock(
                return_value={
                    "runs": [
                        {
                            "tool": {
                                "driver": {
                                    "name": "skims",
                                    "rules": [
                                        {
                                            "id": "001",
                                            "defaultConfiguration": {
                                                "level": "error"
                                            },
                                            "fullDescription": {
                                                "text": "Dynamic SQL statements are generated without the required data validation and without using parameterized statements or stored procedures.\n"  # noqa
                                            },
                                            "help": {
                                                "text": "- Perform queries to the database through sentences or parameterized procedures."  # noqa
                                            },
                                            "helpUri": "https://docs.fluidattacks.com/criteria/vulnerabilities/001#details",  # noqa
                                            "name": "SQL injection - C Sharp SQL API",  # noqa
                                        },
                                    ],
                                }
                            },
                            "originalUriBaseIds": {
                                "SRCROOT": {"uri": "nickname1"}
                            },
                            "results": [
                                {
                                    "message": {
                                        "text": "",
                                        "properties": {},
                                    },
                                    "kind": "open",
                                    "level": "error",
                                    "locations": [
                                        {
                                            "physicalLocation": {
                                                "artifactLocation": {
                                                    "uri": "back/src/index.js"
                                                },
                                                "region": {
                                                    "snippet": {"text": " "},
                                                    "startLine": 24,
                                                },
                                            }
                                        }
                                    ],
                                    "properties": {
                                        "kind": "lines",
                                        "source_method": "conf_files.sensitive_key_in_json",  # noqa
                                        "stream": "skims",
                                        "technique": "BSAST",
                                    },
                                    "ruleId": "001",
                                },
                            ],
                            "taxonomies": [
                                {
                                    "name": "criteria",
                                    "contents": [
                                        "localizedData",
                                        "nonLocalizedData",
                                    ],
                                    "informationUri": "https://docs.fluidattacks.com/criteria/requirements/",  # noqa
                                    "isComprehensive": False,
                                    "organization": "Fluidattcks",
                                    "shortDescription": {
                                        "text": "The fluidattcks security requirements"  # noqa
                                    },
                                    "taxa": [],
                                    "version": "1",
                                }
                            ],
                            "versionControlProvenance": [
                                {
                                    "branch": "master",
                                    "revisionId": "7fd232de194916018c4ba68f5cb6dc595e99df7e",  # noqa
                                }
                            ],
                        }
                    ],
                    "version": "2.1.0",
                    "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.4.json",  # noqa
                }
            ),
        ):
            from schedulers.report_machine import (
                process_execution,
            )

            await process_execution(
                get_new_context(),
                None,
                "group1_1234345",
                criteria_vulns,
                criteria_reqs,
            )
            loaders = get_new_context()
            group_findings: Tuple[
                Finding, ...
            ] = await loaders.group_drafts_and_findings.load("group1")
            group_findings = tuple(
                finding for finding in group_findings if "001" in finding.title
            )

            assert len(group_findings) > 0
            finding = group_findings[0]
            integrates_vulnerabilities: Tuple[Vulnerability, ...] = tuple(
                vuln
                for vuln in await loaders.finding_vulnerabilities.load(
                    finding.id
                )
                if vuln.state.status == VulnerabilityStateStatus.OPEN
                and vuln.state.source == Source.MACHINE
                and vuln.root_id == "88637616-41d4-4242-854a-db8ff7fe1ab6"
            )
            # te execution must close a vulnerability but are in the scope
            assert len(integrates_vulnerabilities) == 2
            loaders = get_new_context()
            assert (
                await loaders.vulnerability.load(
                    "4dbc01e0-4cfc-4b77-9b71-bb7566c60bg"
                )
            ).state.status == VulnerabilityStateStatus.CLOSED
