# -*- coding: utf-8 -*-
import os
import pytest
import shutil
from collections import OrderedDict
from decimal import Decimal
from unittest.mock import patch

from freezegun import freeze_time

from data_containers.toe_inputs import GitRootToeInput
from data_containers.toe_lines import GitRootToeLines
from dataloaders import get_new_context
from findings.domain import get_findings_by_group
from groups import domain as groups_domain
from newutils import (
    datetime as datetime_utils,
    git as git_utils,
)
from organizations.domain import (
    get_id_by_name,
    get_pending_deletion_date_str,
    iterate_organizations,
    update_pending_deletion_date,
)
from toe.inputs import domain as toe_inputs_domain
from toe.lines import domain as toe_lines_domain
from schedulers import (
    delete_imamura_stakeholders,
    delete_obsolete_groups,
    delete_obsolete_orgs,
    toe_inputs_etl,
    toe_lines_etl,
    update_indicators,
)
from users import dal as users_dal
from vulnerabilities.dal import get as get_vuln
from vulnerabilities.domain import list_vulnerabilities_async


pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_status_vulns_by_time_range() -> None:
    released_findings = await get_findings_by_group("UNITTESTING")
    first_day = "2019-01-01 12:00:00"
    last_day = "2019-06-30 23:59:59"
    vulns = await list_vulnerabilities_async(
        [str(finding["finding_id"]) for finding in released_findings],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True,
    )
    test_data = update_indicators.get_status_vulns_by_time_range(
        vulns, first_day, last_day
    )
    expected_output = {"found": 8, "accepted": 2, "closed": 2}
    assert test_data == expected_output


def test_create_weekly_date() -> None:
    first_date = "2019-09-19 13:23:32"
    test_data = update_indicators.create_weekly_date(first_date)
    expected_output = "Sep 16 - 22, 2019"
    assert test_data == expected_output


async def test_get_accepted_vulns() -> None:
    released_findings = await get_findings_by_group("UNITTESTING")
    last_day = "2019-06-30 23:59:59"
    vulns = await list_vulnerabilities_async(
        [str(finding["finding_id"]) for finding in released_findings],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True,
    )
    test_data = sum(
        [
            update_indicators.get_accepted_vulns(vuln, last_day)
            for vuln in vulns
        ]
    )
    expected_output = 2
    assert test_data == expected_output


async def test_get_by_time_range() -> None:
    last_day = "2020-09-09 23:59:59"
    vuln = await get_vuln("80d6a69f-a376-46be-98cd-2fdedcffdcc0")
    test_data = update_indicators.get_by_time_range(vuln[0], last_day)
    expected_output = 1
    assert test_data == expected_output


async def test_create_register_by_week() -> None:
    context = get_new_context()
    project_name = "unittesting"
    test_data = await update_indicators.create_register_by_week(
        context, project_name
    )
    assert isinstance(test_data, list)
    for item in test_data:
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
    vulns = await list_vulnerabilities_async(
        ["422286126"],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True,
    )
    test_data = update_indicators.get_first_week_dates(vulns)
    expected_output = ("2019-12-30 00:00:00", "2020-01-05 23:59:59")
    assert test_data == expected_output


async def test_get_date_last_vulns() -> None:
    vulns = await list_vulnerabilities_async(
        ["422286126"],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True,
    )
    test_data = update_indicators.get_date_last_vulns(vulns)
    expected_output = "2020-09-07 16:01:26"
    assert test_data == expected_output


async def test_get_group_indicators() -> None:
    group_name = "unittesting"
    findings = await get_findings_by_group(group_name)
    vulns = await list_vulnerabilities_async(
        [finding["finding_id"] for finding in findings]
    )
    test_data = await update_indicators.get_group_indicators(group_name)
    over_time = [
        element[-12:] for element in test_data["remediated_over_time"]
    ]
    found = over_time[0][-1]["y"]
    closed = over_time[1][-1]["y"]
    accepted = over_time[2][-1]["y"]

    assert isinstance(test_data, dict)
    assert len(test_data) == 17
    assert test_data["max_open_severity"] == Decimal(6.3).quantize(
        Decimal("0.1")
    )
    assert found == len(
        [
            vuln
            for vuln in vulns
            if vuln["historic_state"][-1].get("state") != "DELETED"
        ]
    )
    assert accepted == len(
        [
            vuln
            for vuln in vulns
            if (
                vuln.get("historic_treatment", [{}])[-1].get("treatment")
                in {"ACCEPTED", "ACCEPTED_UNDEFINED"}
                and vuln["historic_state"][-1].get("state") == "open"
            )
        ]
    )
    assert closed == len(
        [
            vuln
            for vuln in vulns
            if vuln["historic_state"][-1].get("state") == "closed"
        ]
    )


@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_delete_obsolete_orgs() -> None:
    org_id = "ORG#33c08ebd-2068-47e7-9673-e1aa03dc9448"
    org_name = "kiba"
    org_ids = []
    async for organization_id, _ in iterate_organizations():
        org_ids.append(organization_id)
    assert org_id in org_ids
    assert len(org_ids) == 9

    now_str = datetime_utils.get_as_str(datetime_utils.get_now())
    await update_pending_deletion_date(org_id, org_name, now_str)
    await delete_obsolete_orgs.main()
    new_org_ids = []
    async for organization_id, _ in iterate_organizations():
        new_org_ids.append(organization_id)
    assert org_id not in new_org_ids
    assert len(new_org_ids) == 8

    org_id = "ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de"
    org_pending_deletion_date = await get_pending_deletion_date_str(org_id)
    assert org_pending_deletion_date == "2020-01-29 19:00:00"


@pytest.mark.changes_db
@freeze_time("2021-01-01")
async def test_delete_imamura_stakeholders() -> None:
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
    delete_stakeholder = await users_dal.get("deleteimamura@fluidattacks.com")
    delete_stakeholder_exists = bool(delete_stakeholder)
    assert delete_stakeholder_exists
    nodelete_stakeholder = await users_dal.get(
        "nodeleteimamura@fluidattacks.com"
    )
    nodelete_stakeholder_exists = bool(nodelete_stakeholder)
    assert nodelete_stakeholder_exists

    await delete_imamura_stakeholders.main()

    loaders = get_new_context()
    org_stakeholders_loader = loaders.organization_stakeholders
    org_stakeholders = await org_stakeholders_loader.load(org_id)
    org_stakeholders_emails = [
        stakeholder["email"] for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == ["nodeleteimamura@fluidattacks.com"]
    delete_stakeholder = await users_dal.get("deleteimamura@fluidattacks.com")
    delete_stakeholder_exists = bool(delete_stakeholder)
    assert not delete_stakeholder_exists
    nodelete_stakeholder = await users_dal.get(
        "nodeleteimamura@fluidattacks.com"
    )
    nodelete_stakeholder_exists = bool(nodelete_stakeholder)
    assert nodelete_stakeholder_exists


@pytest.mark.changes_db
async def test_delete_obsolete_groups() -> None:
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
            "project_name": "setpendingdeletion",
        },
        {
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
        if group["project_name"] == "setpendingdeletion"
    ][0]
    assert setpendingdeletion["project_status"] == "SUSPENDED"
    assert "pending_deletion_date" in setpendingdeletion
    deletegroup = [
        group for group in groups if group["project_name"] == "deletegroup"
    ][0]
    assert deletegroup["project_status"] == "DELETED"


@pytest.mark.changes_db
async def test_toe_lines_etl() -> None:
    def clone_services_repository_mock(path) -> None:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "mock/test_lines.csv")
        os.makedirs(f"{path}/groups/unittesting/toe")
        shutil.copy2(filename, f"{path}/groups/unittesting/toe/lines.csv")

    group_name = "unittesting"
    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert group_toe_lines == (
        GitRootToeLines(
            comments="comment test",  # NOSONAR
            filename="product/test/test#.config",
            group_name="unittesting",
            loc=8,
            modified_commit="983466z",
            modified_date="2019-08-01T00:00:00-05:00",
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            tested_date="2021-02-28T00:00:00-05:00",
            tested_lines=4,
            sorts_risk_level=0,
        ),
        GitRootToeLines(
            comments="comment test",
            filename="integrates_1/test2/test.sh",
            group_name="unittesting",
            loc=172,
            modified_commit="273412t",
            modified_date="2020-11-19T00:00:00-05:00",
            root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            tested_date="2021-01-20T00:00:00-05:00",
            tested_lines=120,
            sorts_risk_level=0,
        ),
    )

    with patch(
        "newutils.git.clone_services_repository",
        wraps=clone_services_repository_mock,
    ):
        await toe_lines_etl.main()

    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert group_toe_lines == (
        GitRootToeLines(
            comments="comment test 2",
            filename="product/test/test#.config",
            group_name="unittesting",
            loc=8,
            modified_commit="983466z",
            modified_date="2019-08-01T00:00:00-05:00",
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            tested_date="2021-02-28T00:00:00-05:00",
            tested_lines=4,
            sorts_risk_level=0,
        ),
        GitRootToeLines(
            comments="comment test",
            filename="integrates_1/test3/test.sh",
            group_name="unittesting",
            loc=120,
            modified_commit="742412r",
            modified_date="2020-11-19T00:00:00-05:00",
            root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            tested_date="2021-01-22T00:00:00-05:00",
            tested_lines=88,
            sorts_risk_level=0,
        ),
    )


@pytest.mark.changes_db
async def test_toe_inputs_etl(monkeypatch) -> None:
    def mocked_clone_services_repository(path) -> None:
        print("mocked_clone_services_repository")
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
    group_toe_inputs = await toe_inputs_domain.get_by_group(group_name)
    assert group_toe_inputs == (
        GitRootToeInput(
            commit="hh66uu5",
            component="test.com/api/Test",
            created_date="2000-01-01T00:00:00-05:00",  # NOSONAR
            entry_point="idTest",
            group_name="unittesting",
            seen_first_time_by="",
            tested_date="2020-01-02T00:00:00-05:00",
            verified="Yes",
            vulns="FIN.S.0001.Test",
        ),
        GitRootToeInput(
            commit="e91320h",
            component="test.com/test/test.aspx",  # NOSONAR
            created_date="2020-03-14T00:00:00-05:00",
            entry_point="btnTest",
            group_name="unittesting",
            seen_first_time_by="test@test.com",
            tested_date="2021-02-02T00:00:00-05:00",
            verified="No",
            vulns="",
        ),
        GitRootToeInput(
            commit="d83027t",
            component="test.com/test2/test.aspx",
            created_date="2020-01-11T00:00:00-05:00",
            entry_point="-",
            group_name="unittesting",
            seen_first_time_by="test2@test.com",
            tested_date="2021-02-11T00:00:00-05:00",
            verified="No",
            vulns="FIN.S.0003.Test",
        ),
    )
    await toe_inputs_etl.main()
    group_toe_inputs = await toe_inputs_domain.get_by_group(group_name)
    assert group_toe_inputs == (
        GitRootToeInput(
            commit="hh66uu5",
            component="test.com/api/Test",
            created_date="2000-01-01T00:00:00-05:00",
            entry_point="idTest",
            group_name="unittesting",
            seen_first_time_by="",
            tested_date="2020-01-02T00:00:00-05:00",
            verified="Yes",
            vulns="FIN.S.0001.Test",
        ),
        GitRootToeInput(
            commit="r44432f",
            component="test.com/test/test.aspx",
            created_date="2000-01-01T00:00:00-05:00",
            entry_point="",
            group_name="unittesting",
            seen_first_time_by="",
            tested_date="2021-02-11T00:00:00-05:00",
            verified="Yes",
            vulns="FIN.S.0002.Test",
        ),
        GitRootToeInput(
            commit="e91320h",
            component="test.com/test/test.aspx",
            created_date="2020-03-14T00:00:00-05:00",
            entry_point="btnTest",
            group_name="unittesting",
            seen_first_time_by="test@test.com",
            tested_date="2000-01-01T00:00:00-05:00",
            verified="No",
            vulns="",
        ),
    )
