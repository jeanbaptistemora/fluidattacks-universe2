# -*- coding: utf-8 -*-
from _pytest.monkeypatch import (
    MonkeyPatch,
)
from collections import (
    OrderedDict,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.services_toe_lines.types import (
    ServicesToeLines,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_severity_score,
)
from freezegun import (  # type: ignore
    freeze_time,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
    git as git_utils,
    vulnerabilities as vulns_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations.domain import (
    get_id_by_name,
    get_pending_deletion_date_str,
    iterate_organizations,
    update_pending_deletion_date,
)
import os
import pytest
from schedulers import (
    delete_imamura_stakeholders,
    delete_obsolete_groups,
    delete_obsolete_orgs,
    services_toe_lines_etl,
    toe_inputs_etl,
    update_indicators,
)
import shutil
from typing import (
    Dict,
    Tuple,
)
from unittest.mock import (
    patch,
)
from users import (
    dal as users_dal,
)
from vulnerabilities.dal import (
    get as get_vuln,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_status_vulns_by_time_range() -> None:
    first_day = "2019-01-01 12:00:00"
    last_day = "2019-06-30 23:59:59"
    loaders = get_new_context()
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        "unittesting"
    )
    vulns = await loaders.finding_vulns_nzr.load_many_chained(
        [finding.id for finding in findings]
    )
    findings_severity: Dict[str, Decimal] = {
        finding.id: get_severity_score(finding.severity)
        for finding in findings
    }
    vulnerabilities_severity = [
        findings_severity[str(vulnerability["finding_id"])]
        for vulnerability in vulns
    ]
    historic_states = [
        vulns_utils.sort_historic_by_date(vulnerability["historic_state"])
        for vulnerability in vulns
    ]
    test_data = update_indicators.get_status_vulns_by_time_range(
        vulnerabilities=vulns,
        vulnerabilities_severity=vulnerabilities_severity,
        vulnerabilities_historic_states=historic_states,
        first_day=first_day,
        last_day=last_day,
    )
    expected_output = {"found": 8, "accepted": 2, "closed": 2}
    output = {
        "found": test_data.found_vulnerabilities,
        "accepted": test_data.accepted_vulnerabilities,
        "closed": test_data.closed_vulnerabilities,
    }
    assert sorted(output) == sorted(expected_output)


def test_create_weekly_date() -> None:
    first_date = "2019-09-19 13:23:32"
    test_data = update_indicators.create_weekly_date(first_date)
    expected_output = "Sep 16 - 22, 2019"
    assert test_data == expected_output


async def test_get_accepted_vulns() -> None:
    loaders = get_new_context()
    last_day = "2019-06-30 23:59:59"
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        "unittesting"
    )
    vulnerabilties = await loaders.finding_vulns_nzr.load_many_chained(
        [finding.id for finding in findings]
    )
    findings_severity: Dict[str, Decimal] = {
        finding.id: get_severity_score(finding.severity)
        for finding in findings
    }
    vulnerabilities_severity = [
        findings_severity[str(vulnerability["finding_id"])]
        for vulnerability in vulnerabilties
    ]
    historic_states = [
        vulns_utils.sort_historic_by_date(vulnerability["historic_state"])
        for vulnerability in vulnerabilties
    ]
    test_data = sum(
        [
            update_indicators.get_accepted_vulns(
                vulnerability, historic_state, severity, last_day
            ).vulnerabilities
            for vulnerability, historic_state, severity in zip(
                vulnerabilties,
                historic_states,
                vulnerabilities_severity,
            )
        ]
    )
    expected_output = 2
    assert test_data == expected_output


async def test_get_by_time_range() -> None:
    loaders = get_new_context()
    last_day = "2020-09-09 23:59:59"
    vulnerability = (await get_vuln("80d6a69f-a376-46be-98cd-2fdedcffdcc0"))[0]
    finding: Finding = await loaders.finding.load(vulnerability["finding_id"])
    vulnerability_severity = get_severity_score(finding.severity)
    test_data = update_indicators.get_by_time_range(
        vulns_utils.sort_historic_by_date(vulnerability["historic_state"]),
        vulnerability_severity,
        last_day,
    )
    expected_output = 1
    assert test_data.vulnerabilities == expected_output


async def test_create_register_by_week() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    test_data = await update_indicators.create_register_by_week(
        loaders, group_name
    )
    assert isinstance(test_data.vulnerabilities, list)
    for item in test_data.vulnerabilities:
        assert isinstance(item, list)
        assert isinstance(item[0], dict)
        assert item[0] is not None


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
    test_data = update_indicators.create_data_format_chart(registers)
    expected_output = [
        [{"y": 2, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 0, "x": "Sep 24 - 30, 2018"}],
        [{"y": 2, "x": "Sep 24 - 30, 2018"}],
    ]
    assert test_data == expected_output


async def test_get_first_week_dates() -> None:
    loaders: Dataloaders = get_new_context()
    finding_id = "422286126"
    vulns = await loaders.finding_vulns.load(finding_id)
    test_data = update_indicators.get_first_week_dates(vulns)
    expected_output = ("2019-12-30 00:00:00", "2020-01-05 23:59:59")
    assert test_data == expected_output


async def test_get_date_last_vulns() -> None:
    loaders: Dataloaders = get_new_context()
    finding_id = "422286126"
    vulns = await loaders.finding_vulns.load(finding_id)
    test_data = update_indicators.get_date_last_vulns(vulns)
    expected_output = "2020-09-07 16:01:26"
    assert test_data == expected_output


async def test_get_group_indicators() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    vulnerabilties = await loaders.finding_vulns_nzr.load_many_chained(
        [finding.id for finding in findings]
    )
    test_data = await update_indicators.get_group_indicators(group_name)
    over_time = [
        element[-12:] for element in test_data["remediated_over_time"]
    ]
    found = over_time[0][-1]["y"]
    closed = over_time[1][-1]["y"]
    accepted = over_time[2][-1]["y"]

    assert isinstance(test_data, dict)
    assert len(test_data) == 26
    assert test_data["max_open_severity"] == Decimal(6.3).quantize(
        Decimal("0.1")
    )
    assert test_data["open_findings"] == 5
    assert found == len(
        [
            vulnerability
            for vulnerability in vulnerabilties
            if vulnerability["historic_state"][-1].get("state") != "DELETED"
        ]
    )
    assert accepted == len(
        [
            vulnerability
            for vulnerability in vulnerabilties
            if (
                vulnerability.get("historic_treatment", [{}])[-1].get(
                    "treatment"
                )
                in {"ACCEPTED", "ACCEPTED_UNDEFINED"}
                and vulnerability["historic_state"][-1].get("state") == "open"
            )
        ]
    )
    assert closed == len(
        [
            vulnerability
            for vulnerability in vulnerabilties
            if vulnerability["historic_state"][-1].get("state") == "closed"
        ]
    )
    test_imamura_data = await update_indicators.get_group_indicators(
        "deleteimamura"
    )
    assert isinstance(test_imamura_data, dict)
    assert len(test_imamura_data) == 26


@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_delete_obsolete_orgs() -> None:
    org_id = "ORG#d32674a9-9838-4337-b222-68c88bf54647"
    org_name = "makoto"
    org_ids = []
    async for organization_id, _ in iterate_organizations():
        org_ids.append(organization_id)
    assert org_id in org_ids
    assert len(org_ids) == 10

    now_str = datetime_utils.get_as_str(datetime_utils.get_now())
    await update_pending_deletion_date(org_id, org_name, now_str)
    await delete_obsolete_orgs.main()
    new_org_ids = []
    async for organization_id, _ in iterate_organizations():
        new_org_ids.append(organization_id)
    assert org_id not in new_org_ids
    assert len(new_org_ids) == 9

    org_id = "ORG#ffddc7a3-7f05-4fc7-b65d-7defffa883c2"
    org_pending_deletion_date = await get_pending_deletion_date_str(org_id)
    assert org_pending_deletion_date == "2020-01-29 19:00:00"


@pytest.mark.changes_db
@freeze_time("2021-01-01")
async def test_remove_imamura_stakeholders() -> None:
    org_name = "imamura"
    org_id = await get_id_by_name(org_name)
    loaders = get_new_context()
    org_stakeholders_loader = loaders.organization_stakeholders
    org_stakeholders = await org_stakeholders_loader.load(org_id)
    org_stakeholders_emails = [
        stakeholder["email"] for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == [
        "deleteimamura@fluidattacks.com",  # NOSONAR
        "nodeleteimamura@fluidattacks.com",  # NOSONAR
    ]
    remove_stakeholder = await users_dal.get("deleteimamura@fluidattacks.com")
    remove_stakeholder_exists = bool(remove_stakeholder)
    assert remove_stakeholder_exists
    noremove_stakeholder = await users_dal.get(
        "nodeleteimamura@fluidattacks.com"
    )
    noremove_stakeholder_exists = bool(noremove_stakeholder)
    assert noremove_stakeholder_exists

    await delete_imamura_stakeholders.main()

    loaders = get_new_context()
    org_stakeholders_loader = loaders.organization_stakeholders
    org_stakeholders = await org_stakeholders_loader.load(org_id)
    org_stakeholders_emails = [
        stakeholder["email"] for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == ["nodeleteimamura@fluidattacks.com"]
    remove_stakeholder = await users_dal.get("deleteimamura@fluidattacks.com")
    remove_stakeholder_exists = bool(remove_stakeholder)
    assert not remove_stakeholder_exists
    noremove_stakeholder = await users_dal.get(
        "nodeleteimamura@fluidattacks.com"
    )
    noremove_stakeholder_exists = bool(noremove_stakeholder)
    assert noremove_stakeholder_exists


@pytest.mark.changes_db
async def test_remove_obsolete_groups() -> None:
    group_attributes = {
        "project_name",
        "project_status",
        "pending_deletion_date",
    }
    alive_groups = await groups_domain.get_alive_groups(group_attributes)
    assert len(alive_groups) == 13
    expected_groups = [
        {
            "project_status": "SUSPENDED",
            "group_name": "setpendingdeletion",
            "project_name": "setpendingdeletion",
        },
        {
            "group_name": "deletegroup",
            "project_name": "deletegroup",
            "project_status": "ACTIVE",
            "pending_deletion_date": "2020-12-22 14:36:29",
        },
    ]
    for expected_group in expected_groups:
        assert expected_group in alive_groups

    await delete_obsolete_groups.main()

    alive_groups = await groups_domain.get_alive_groups(group_attributes)
    assert len(alive_groups) == 12
    groups = await groups_domain.get_all(group_attributes)
    setpendingdeletion = [
        group
        for group in groups
        if get_key_or_fallback(group) == "setpendingdeletion"
    ][0]
    assert setpendingdeletion["project_status"] == "SUSPENDED"
    assert "pending_deletion_date" in setpendingdeletion
    deletegroup = [
        group
        for group in groups
        if get_key_or_fallback(group) == "deletegroup"
    ][0]
    assert deletegroup["project_status"] == "DELETED"


@pytest.mark.changes_db
async def test_toe_lines_etl() -> None:
    def clone_services_repository_mock(path: str) -> None:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "mock/test_lines.csv")
        os.makedirs(f"{path}/groups/unittesting/toe")
        shutil.copy2(filename, f"{path}/groups/unittesting/toe/lines.csv")

    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_lines = await loaders.group_services_toe_lines.load(group_name)
    assert group_toe_lines == (
        ServicesToeLines(
            comments="comment test",  # NOSONAR
            filename="test/test#.config",
            group_name="unittesting",
            loc=8,
            modified_commit="983466z",
            modified_date="2019-08-01T05:00:00+00:00",
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            tested_date="2021-02-28T05:00:00+00:00",
            tested_lines=4,
            sorts_risk_level=0,
        ),
        ServicesToeLines(
            comments="comment test",
            filename="test2/test.sh",
            group_name="unittesting",
            loc=172,
            modified_commit="273412t",
            modified_date="2020-11-19T05:00:00+00:00",
            root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            tested_date="2021-01-20T05:00:00+00:00",
            tested_lines=120,
            sorts_risk_level=0,
        ),
    )

    with patch(
        "newutils.git.clone_services_repository",
        wraps=clone_services_repository_mock,
    ):
        await services_toe_lines_etl.main()

    loaders = get_new_context()
    group_toe_lines = await loaders.group_services_toe_lines.load(group_name)
    assert group_toe_lines == (
        ServicesToeLines(
            comments="comment test 2",
            filename="test/test#.config",
            group_name="unittesting",
            loc=8,
            modified_commit="983466z",
            modified_date="2019-08-01T05:00:00+00:00",
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            tested_date="2021-02-28T05:00:00+00:00",
            tested_lines=4,
            sorts_risk_level=0,
        ),
        ServicesToeLines(
            comments="comment test",
            filename="test3/test.sh",
            group_name="unittesting",
            loc=120,
            modified_commit="742412r",
            modified_date="2020-11-19T05:00:00+00:00",
            root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            tested_date="2021-01-22T05:00:00+00:00",
            tested_lines=88,
            sorts_risk_level=-1,
        ),
    )


@pytest.mark.changes_db
async def test_toe_inputs_etl(monkeypatch: MonkeyPatch) -> None:
    def mocked_clone_services_repository(path: str) -> None:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "mock/test_inputs.csv")
        os.makedirs(f"{path}/groups/unittesting/toe")
        shutil.copy2(filename, f"{path}/groups/unittesting/toe/inputs.csv")

    monkeypatch.setattr(
        git_utils,
        "clone_services_repository",
        mocked_clone_services_repository,
    )
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load(group_name)
    assert group_toe_inputs == (
        ToeInput(
            commit="hh66uu5",
            component="test.com/api/Test",
            created_date="2000-01-01T05:00:00+00:00",  # NOSONAR
            entry_point="idTest",
            group_name="unittesting",
            seen_first_time_by="",
            tested_date="2020-01-02T00:00:00-05:00",
            unreliable_root_id="",
            verified="Yes",
            vulns="FIN.S.0001.Test",
        ),
        ToeInput(
            commit="e91320h",
            component="test.com/test/test.aspx",  # NOSONAR
            created_date="2020-03-14T00:00:00-05:00",
            entry_point="btnTest",
            group_name="unittesting",
            seen_first_time_by="test@test.com",
            tested_date="2021-02-02T00:00:00-05:00",
            unreliable_root_id="",
            verified="No",
            vulns="",
        ),
        ToeInput(
            commit="d83027t",
            component="test.com/test2/test.aspx",
            created_date="2020-01-11T00:00:00-05:00",
            entry_point="-",
            group_name="unittesting",
            seen_first_time_by="test2@test.com",
            tested_date="2021-02-11T00:00:00-05:00",
            unreliable_root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            verified="No",
            vulns="FIN.S.0003.Test",
        ),
    )
    await toe_inputs_etl.main()
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load(group_name)
    assert group_toe_inputs == (
        ToeInput(
            commit="hh66uu5",
            component="test.com/api/Test",
            created_date="2000-01-01T05:00:00+00:00",
            entry_point="idTest",
            group_name="unittesting",
            seen_first_time_by="",
            tested_date="2020-01-02T05:00:00+00:00",
            unreliable_root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            verified="Yes",
            vulns="FIN.S.0001.Test",
        ),
        ToeInput(
            commit="r44432f",
            component="test.com/test/test.aspx",
            created_date="2000-01-01T05:00:00+00:00",
            entry_point="",
            group_name="unittesting",
            seen_first_time_by="",
            tested_date="2021-02-11T05:00:00+00:00",
            unreliable_root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            verified="Yes",
            vulns="FIN.S.0002.Test",
        ),
        ToeInput(
            commit="e91320h",
            component="test.com/test/test.aspx",
            created_date="2020-03-14T05:00:00+00:00",
            entry_point="btnTest",
            group_name="unittesting",
            seen_first_time_by="test@test.com",
            tested_date="2000-01-01T05:00:00+00:00",
            unreliable_root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            verified="No",
            vulns="",
        ),
    )
