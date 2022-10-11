# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from finding_comments import (
    domain as comments_domain,
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
@pytest.mark.resolver_test_group("report_machine_s3")
async def test_persist_result(populate: bool) -> None:
    assert populate
    criteria_vulns = await get_vulns_file()
    criteria_reqs = await get_requirements_file()
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
                                        "text": "sql injection in back/src/index.js line 24",  # noqa
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
                                        "method_developer": "asalgado@fluidattacks.com",  # noqa
                                        "source_method": "conf_files.sensitive_key_in_json",  # noqa
                                        "stream": "skims",
                                        "technique": "BSAST",
                                    },
                                    "ruleId": "001",
                                },
                                {
                                    "message": {
                                        "text": "sql injection in back/src/index.js line 35",  # noqa
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
                                                    "startLine": 35,
                                                },
                                            }
                                        }
                                    ],
                                    "properties": {
                                        "kind": "lines",
                                        "method_developer": "asalgado@fluidattacks.com",  # noqa
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
            assert len(integrates_vulnerabilities) == 3
            loaders = get_new_context()
            # te execution must close a vulnerability but are in the scope
            assert (
                await loaders.vulnerability.load(
                    "4dbc01e0-4cfc-4b77-9b71-bb7566c60bg"
                )
            ).state.status == VulnerabilityStateStatus.CLOSED
            vuln_state = await loaders.vulnerability_historic_state.load(
                "4dbc01e0-4cfc-4b77-9b71-bb7566c60bg"
            )
            assert (
                vuln_state[-1].commit
                == "7fd232de194916018c4ba68f5cb6dc595e99df7e"
            )
            assert finding.evidences.evidence5 is not None
            assert finding.evidences.evidence1 is None
            assert (
                "sql injection in" in finding.evidences.evidence5.description
            )

            comments = await comments_domain.get_comments(
                loaders=loaders,
                group_name="group1",
                finding_id=finding.id,
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
    criteria_vulns = await get_vulns_file()
    criteria_reqs = await get_requirements_file()
    with mock.patch(
        "schedulers.report_machine.get_config",
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
            "schedulers.report_machine.get_sarif_log",
            side_effect=mock.AsyncMock(
                return_value={
                    "runs": [
                        {
                            "tool": {
                                "driver": {
                                    "name": "skims",
                                    "contents": [
                                        "localizedData",
                                        "nonLocalizedData",
                                    ],
                                    "rules": [
                                        {
                                            "id": "079",
                                            "defaultConfiguration": {
                                                "level": "error"
                                            },
                                            "fullDescription": {
                                                "text": "Dependencies are not explicitly declared (name and version) within the source code. They are copied directly into the repositories.\n"  # noqa
                                            },
                                            "help": {
                                                "text": "All dependencies must be declared and must referenced with a dependency manager (npm, pip, maven). This allows to standardize projects construction and packaging.\n"  # noqa
                                            },
                                            "helpUri": "https://docs.fluidattacks.com/criteria/vulnerabilities/079#details",  # noqa
                                            "name": "Non-upgradable dependencies",  # noqa
                                            "properties": {
                                                "auto_approve": "true"
                                            },
                                        }
                                    ],
                                }
                            },
                            "newlineSequences": ["\r\n", "\n"],
                            "originalUriBaseIds": {
                                "SRCROOT": {"uri": "universe"}
                            },
                            "results": [
                                {
                                    "message": {
                                        "text": "The dependency is not explicitly declared in your requirements.txt in universe/skims/test/data/lib_path/f011/requirements.txt",  # noqa
                                        "properties": {
                                            "dependency_name": "decorator"
                                        },
                                    },
                                    "kind": "open",
                                    "level": "error",
                                    "locations": [
                                        {
                                            "physicalLocation": {
                                                "artifactLocation": {
                                                    "uri": "skims/test/data/lib_path/f011/requirements.txt"  # noqa
                                                },
                                                "region": {
                                                    "snippet": {
                                                        "text": "  1 | aioextensions==21.7.2261349\n  2 | apk-signer==1.1.1\n  3 | apturl==0.5.2\n  4 | asn1crypto==1.4.0\n  5 | Pillow==6.0.0\n    ^ Col 0"  # noqa
                                                    },
                                                    "startLine": 0,
                                                },
                                            }
                                        }
                                    ],
                                    "properties": {
                                        "kind": "lines",
                                        "method_developer": "lsaavedra@fluidattacks.com",  # noqa
                                        "source_method": "python.pip_incomplete_dependencies_list",  # noqa
                                        "stream": "skims",
                                        "technique": "BSAST",
                                    },
                                    "ruleId": "079",
                                    "taxa": [
                                        {
                                            "id": "302",
                                            "toolComponent": {
                                                "name": "criteria"
                                            },
                                        }
                                    ],
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
                                    "isComprehensive": "false",
                                    "organization": "Fluidattcks",
                                    "shortDescription": {
                                        "text": "The fluidattcks security requirements"  # noqa
                                    },
                                    "taxa": [
                                        {
                                            "id": "302",
                                            "fullDescription": {
                                                "text": "The usage of third-party software and libraries is very common in modern applications, as it greatly reduces the effort required to develop them. Unfortunately, this software may introduce vulnerabilities into the application, which causes it to require frequent updates. In order to ease the constant update process, instead of directly including third-party software source code in application repositories, it should merely be referenced and managed using a package manager.\n"  # noqa
                                            },
                                            "helpUri": "https://docs.fluidattacks.com/criteria/requirements/302",  # noqa
                                            "name": "Declare dependencies explicitly",  # noqa
                                            "shortDescription": {
                                                "text": "All dependencies (third-party software/libraries) must be explicitly declared (name and specific version) in a file inside the source code repository. Their source code must not be directly included in the repository.\n"  # noqa
                                            },
                                        }
                                    ],
                                    "version": "1",
                                }
                            ],
                            "versionControlProvenance": [
                                {
                                    "repositoryUri": "https://gitlab.com/fluidattacks/universe.git",  # noqa
                                    "branch": "lsaavedraatfluid",
                                    "revisionId": "6e38c1c855ff9d87f9e51247a23fb17d5ae9b617",  # noqa
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
                "group1_1234345",
                criteria_vulns,
                criteria_reqs,
            )
            loaders = get_new_context()
            group_findings: Tuple[
                Finding, ...
            ] = await loaders.group_drafts_and_findings.load("group1")
            group_findings = tuple(
                finding for finding in group_findings if "079" in finding.title
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
            )

            assert len(integrates_vulnerabilities) == 1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine_s3")
async def test_duplicated_reports(populate: bool) -> None:
    assert populate
    criteria_vulns = await get_vulns_file()
    criteria_reqs = await get_requirements_file()
    with mock.patch(
        "schedulers.report_machine.get_config",
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
        "schedulers.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(
            side_effect=[
                {
                    "runs": [
                        {
                            "tool": {
                                "driver": {
                                    "name": "skims",
                                    "contents": [
                                        "localizedData",
                                        "nonLocalizedData",
                                    ],
                                    "rules": [
                                        {
                                            "id": "011",
                                            "defaultConfiguration": {
                                                "level": "error"
                                            },
                                            "fullDescription": {
                                                "text": "The system uses the version of a software or dependency with known vulnerabilities.\n"  # noqa
                                            },
                                            "help": {
                                                "text": "Update the affected software to the versions recommended by the vendor.\n"  # noqa
                                            },
                                            "helpUri": "https://docs.fluidattacks.com/criteria/vulnerabilities/011#details",  # noqa
                                            "name": "Use of software with known vulnerabilities",  # noqa
                                            "properties": {
                                                "auto_approve": "true"
                                            },
                                        }
                                    ],
                                }
                            },
                            "newlineSequences": ["\r\n", "\n"],
                            "originalUriBaseIds": {
                                "SRCROOT": {"uri": "universe"}
                            },
                            "results": [
                                {
                                    "message": {
                                        "text": "Use of io.springfox:springfox-swagger-ui at version 2.6.1 with ['CVE-2019-17495', 'SNYK-JAVA-IOSPRINGFOX-1075064'] in universe/skims/test/data/lib_path/f011/build.gradle",  # noqa
                                        "properties": {
                                            "dependency_name": "io.springfox:springfox-swagger-ui",  # noqa
                                            "dependency_version": "2.6.1",
                                            "cve": [
                                                "CVE-2019-17495",
                                                "SNYK-JAVA-IOSPRINGFOX-1075064",  # noqa
                                            ],
                                        },
                                    },
                                    "kind": "open",
                                    "level": "error",
                                    "locations": [
                                        {
                                            "physicalLocation": {
                                                "artifactLocation": {
                                                    "uri": "skims/test/data/lib_path/f011/build.gradle"  # noqa
                                                },
                                                "region": {
                                                    "snippet": {
                                                        "text": "  1 | dependencies {\n> 2 |     compile \"io.springfox:springfox-swagger-ui:2.6.1\"\n  3 |     compile(\"io.springfox:springfox-swagger-ui\")\n  4 |     compile(group: 'javax.mail', name: 'mail')\n  5 |     compileOnly group: 'org.apache.logging.log4j', name: 'log4j-core', version: '2.13.2'\n  6 |     implementation group: 'org.json', name: 'json', version: '20160810'\n  7 |     implementation(group: 'javax.mail', name: 'mail', version: '1.4')\n  8 | }\n    ^ Col 0"  # noqa
                                                    },
                                                    "startLine": 2,
                                                },
                                            }
                                        }
                                    ],
                                    "properties": {
                                        "kind": "lines",
                                        "method_developer": "acuberos@fluidattacks.com",  # noqa
                                        "source_method": "maven.maven_gradle",
                                        "stream": "skims",
                                        "technique": "SCA",
                                    },
                                    "ruleId": "011",
                                    "taxa": [
                                        {
                                            "id": "262",
                                            "toolComponent": {
                                                "name": "criteria"
                                            },
                                        }
                                    ],
                                }
                            ],
                            "taxonomies": [
                                {
                                    "name": "criteria",
                                    "contents": [
                                        "localizedData",
                                        "nonLocalizedData",
                                    ],
                                    "informationUri": "https://docs.fluidattacks.com/criteria/requirements/",  # noqa
                                    "isComprehensive": "false",
                                    "organization": "Fluidattcks",
                                    "shortDescription": {
                                        "text": "The fluidattcks security requirements"  # noqa
                                    },
                                    "taxa": [
                                        {
                                            "id": "262",
                                            "fullDescription": {
                                                "text": "- The organization must ensure that the version of all of its products and the products provided by third-parties is up to date, stable and tested. This reduces the risk of including vulnerabilities reported in previous versions.\n- When a product changes its version, the implemented improvements must be checked to verify if there were fixes or new controls related to recently discovered vulnerabilities.\n"  # noqa
                                            },
                                            "helpUri": "https://docs.fluidattacks.com/criteria/requirements/262",  # noqa
                                            "name": "Verify third-party components",  # noqa
                                            "shortDescription": {
                                                "text": "The system must use stable, tested and up-to-date versions of third-party components.\n"  # noqa
                                            },
                                        }
                                    ],
                                    "version": "1",
                                }
                            ],
                            "versionControlProvenance": [
                                {
                                    "repositoryUri": "ssh://git@gitlab.com:fluidattacks/product.git",  # noqa
                                    "branch": "atrujilloatfluid",
                                    "revisionId": "fb7ab9254a643cd324a2d8d243ac76be7400dc0b",  # noqa
                                }
                            ],
                        }
                    ],
                    "version": "2.1.0",
                    "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.4.json",  # noqa
                },
                {
                    "runs": [
                        {
                            "tool": {
                                "driver": {
                                    "name": "skims",
                                    "contents": [
                                        "localizedData",
                                        "nonLocalizedData",
                                    ],
                                    "rules": [
                                        {
                                            "id": "011",
                                            "defaultConfiguration": {
                                                "level": "error"
                                            },
                                            "fullDescription": {
                                                "text": "The system uses the version of a software or dependency with known vulnerabilities.\n"  # noqa
                                            },
                                            "help": {
                                                "text": "Update the affected software to the versions recommended by the vendor.\n"  # noqa
                                            },
                                            "helpUri": "https://docs.fluidattacks.com/criteria/vulnerabilities/011#details",  # noqa
                                            "name": "Use of software with known vulnerabilities",  # noqa
                                            "properties": {
                                                "auto_approve": "true"
                                            },
                                        }
                                    ],
                                }
                            },
                            "newlineSequences": ["\r\n", "\n"],
                            "originalUriBaseIds": {
                                "SRCROOT": {"uri": "universe"}
                            },
                            "results": [
                                {
                                    "message": {
                                        "text": "Use of io.springfox:springfox-swagger-ui at version 2.6.1 with ['CVE-2019-17495', 'SNYK-JAVA-IOSPRINGFOX-1075064', 'CVE-2019-TEST'] in universe/skims/test/data/lib_path/f011/build.gradle",  # noqa
                                        "properties": {
                                            "dependency_name": "io.springfox:springfox-swagger-ui",  # noqa
                                            "dependency_version": "2.6.1",
                                            "cve": [
                                                "CVE-2019-17495",
                                                "SNYK-JAVA-IOSPRINGFOX-1075064",  # noqa
                                                "CVE-2019-TEST",
                                            ],
                                        },
                                    },
                                    "kind": "open",
                                    "level": "error",
                                    "locations": [
                                        {
                                            "physicalLocation": {
                                                "artifactLocation": {
                                                    "uri": "skims/test/data/lib_path/f011/build.gradle"  # noqa
                                                },
                                                "region": {
                                                    "snippet": {
                                                        "text": "  1 | dependencies {\n> 2 |     compile \"io.springfox:springfox-swagger-ui:2.6.1\"\n  3 |     compile(\"io.springfox:springfox-swagger-ui\")\n  4 |     compile(group: 'javax.mail', name: 'mail')\n  5 |     compileOnly group: 'org.apache.logging.log4j', name: 'log4j-core', version: '2.13.2'\n  6 |     implementation group: 'org.json', name: 'json', version: '20160810'\n  7 |     implementation(group: 'javax.mail', name: 'mail', version: '1.4')\n  8 | }\n    ^ Col 0"  # noqa
                                                    },
                                                    "startLine": 2,
                                                },
                                            }
                                        }
                                    ],
                                    "properties": {
                                        "kind": "lines",
                                        "method_developer": "acuberos@fluidattacks.com",  # noqa
                                        "source_method": "maven.maven_gradle",
                                        "stream": "skims",
                                        "technique": "SCA",
                                    },
                                    "ruleId": "011",
                                    "taxa": [
                                        {
                                            "id": "262",
                                            "toolComponent": {
                                                "name": "criteria"
                                            },
                                        }
                                    ],
                                }
                            ],
                            "taxonomies": [
                                {
                                    "name": "criteria",
                                    "contents": [
                                        "localizedData",
                                        "nonLocalizedData",
                                    ],
                                    "informationUri": "https://docs.fluidattacks.com/criteria/requirements/",  # noqa
                                    "isComprehensive": "false",
                                    "organization": "Fluidattcks",
                                    "shortDescription": {
                                        "text": "The fluidattcks security requirements"  # noqa
                                    },
                                    "taxa": [
                                        {
                                            "id": "262",
                                            "fullDescription": {
                                                "text": "- The organization must ensure that the version of all of its products and the products provided by third-parties is up to date, stable and tested. This reduces the risk of including vulnerabilities reported in previous versions.\n- When a product changes its version, the implemented improvements must be checked to verify if there were fixes or new controls related to recently discovered vulnerabilities.\n"  # noqa
                                            },
                                            "helpUri": "https://docs.fluidattacks.com/criteria/requirements/262",  # noqa
                                            "name": "Verify third-party components",  # noqa
                                            "shortDescription": {
                                                "text": "The system must use stable, tested and up-to-date versions of third-party components.\n"  # noqa
                                            },
                                        }
                                    ],
                                    "version": "1",
                                }
                            ],
                            "versionControlProvenance": [
                                {
                                    "repositoryUri": "ssh://git@gitlab.com:fluidattacks/product.git",  # noqa
                                    "branch": "atrujilloatfluid",
                                    "revisionId": "fb7ab9254a643cd324a2d8d243ac76be7400dc0b",  # noqa
                                }
                            ],
                        }
                    ],
                    "version": "2.1.0",
                    "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.4.json",  # noqa
                },
            ],
        ),
    ):
        from schedulers.report_machine import (
            process_execution,
        )

        await process_execution(
            "group1_1234345",
            criteria_vulns,
            criteria_reqs,
        )
        loaders = get_new_context()
        group_findings: Tuple[
            Finding, ...
        ] = await loaders.group_drafts_and_findings.load("group1")
        group_findings = tuple(
            finding for finding in group_findings if "011" in finding.title
        )

        assert len(group_findings) > 0
        finding = group_findings[0]
        integrates_vulnerabilities: Tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(finding.id)
            if vuln.state.status == VulnerabilityStateStatus.OPEN
            and vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities) == 1
        where_1 = integrates_vulnerabilities[0].where
        await process_execution(
            "group1",
            criteria_vulns,
            criteria_reqs,
        )
        integrates_vulnerabilities_2: Tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(finding.id)
            if vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities_2) == 1
        where_2 = integrates_vulnerabilities_2[0].where
        assert where_1 == where_2
