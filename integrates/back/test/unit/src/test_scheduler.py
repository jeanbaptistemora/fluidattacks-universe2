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
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
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
from freezegun import (  # type: ignore
    freeze_time,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from organizations.domain import (
    get_id_by_name,
    get_pending_deletion_date_str,
    iterate_organizations,
    update_pending_deletion_date,
)
import pytest
from schedulers import (
    delete_imamura_stakeholders,
    delete_obsolete_groups,
    delete_obsolete_orgs,
    update_indicators,
    update_portfolios,
)
from users import (
    dal as users_dal,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_status_vulns_by_time_range() -> None:
    first_day = "2019-01-01 12:00:00"
    last_day = "2019-06-30 23:59:59"
    loaders = get_new_context()
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        "unittesting"
    )
    vulns = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in findings]
    )
    findings_severity: dict[str, Decimal] = {
        finding.id: get_severity_score(finding.severity)
        for finding in findings
    }
    vulnerabilities_severity = [
        findings_severity[vulnerability.finding_id] for vulnerability in vulns
    ]
    historic_states = await loaders.vulnerability_historic_state.load_many(
        [vuln.id for vuln in vulns]
    )
    historic_treatments = (
        await loaders.vulnerability_historic_treatment.load_many(
            [vuln.id for vuln in vulns]
        )
    )

    test_data = update_indicators.get_status_vulns_by_time_range(
        vulnerabilities=vulns,
        vulnerabilities_severity=vulnerabilities_severity,
        vulnerabilities_historic_states=historic_states,
        vulnerabilities_historic_treatments=historic_treatments,
        first_day=first_day,
        last_day=last_day,
    )
    expected_output = {"found": 4, "accepted": 2, "closed": 1, "opened": 2}
    output = {
        "found": test_data.found_vulnerabilities,
        "accepted": test_data.accepted_vulnerabilities,
        "closed": test_data.closed_vulnerabilities,
        "opened": test_data.open_vulnerabilities,
    }
    expected_output_cvssf = {
        "found": Decimal("51.534"),
        "accepted": Decimal("25.767"),
        "closed": Decimal("1.516"),
        "opened": Decimal("25.122"),
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


def test_create_weekly_date() -> None:
    first_date = "2019-09-19 13:23:32"
    test_data = update_indicators.create_weekly_date(first_date)
    expected_output = "Sep 16 - 22, 2019"
    assert test_data == expected_output


async def test_get_accepted_vulns() -> None:
    loaders = get_new_context()
    last_day = "2019-06-30 23:59:59"
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
            update_indicators.get_accepted_vulns(
                historic_state, historic_treatment, severity, last_day
            ).vulnerabilities
            for historic_state, historic_treatment, severity in zip(
                historic_states,
                historic_treatments,
                vulnerabilities_severity,
            )
        ]
    )
    expected_output = 2
    assert test_data == expected_output


async def test_get_by_time_range() -> None:
    loaders = get_new_context()
    last_day = "2020-09-09 23:59:59"
    vulnerability: Vulnerability = await loaders.vulnerability.load(
        "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    )
    finding: Finding = await loaders.finding.load(vulnerability.finding_id)
    vulnerability_severity = get_severity_score(finding.severity)
    historic_state = await loaders.vulnerability_historic_state.load(
        vulnerability.id
    )
    test_data = update_indicators.get_by_time_range(
        historic_state,
        VulnerabilityStateStatus.OPEN,
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
    vulns = await loaders.finding_vulnerabilities.load(finding_id)
    test_data = update_indicators.get_first_week_dates(vulns)
    expected_output = ("2019-12-30 00:00:00", "2020-01-05 23:59:59")
    assert test_data == expected_output


async def test_get_date_last_vulns() -> None:
    loaders: Dataloaders = get_new_context()
    finding_id = "422286126"
    vulns = await loaders.finding_vulnerabilities.load(finding_id)
    test_data = update_indicators.get_date_last_vulns(vulns)
    expected_output = "2020-09-07 16:01:26"
    assert test_data == expected_output


@pytest.mark.changes_db
@freeze_time("2022-04-20")
async def test_update_group_indicators() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "unittesting"
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    vulnerabilities = (
        await loaders.finding_vulnerabilities_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )

    await update_indicators.main()

    test_data: GroupUnreliableIndicators = (
        await loaders.group_indicators_typed.load(group_name)
    )
    assert len(test_data) == 27
    assert test_data.last_closed_vulnerability_days == 946
    assert test_data.last_closed_vulnerability_finding == "457497316"
    assert test_data.max_open_severity == Decimal(6.3).quantize(Decimal("0.1"))
    assert test_data.closed_vulnerabilities == 7
    assert test_data.open_vulnerabilities == 29
    assert test_data.open_findings == 5
    assert test_data.mean_remediate == Decimal("790")
    assert test_data.mean_remediate_critical_severity == Decimal("0")
    assert test_data.mean_remediate_high_severity == Decimal("0")
    assert test_data.mean_remediate_low_severity == Decimal("800")
    assert test_data.mean_remediate_medium_severity == Decimal("748")
    assert test_data.treatment_summary == GroupTreatmentSummary(
        accepted=2, accepted_undefined=1, in_progress=1, new=25
    )

    over_time = [element[-12:] for element in test_data.remediated_over_time]
    found = over_time[0][-1]["y"]
    closed = over_time[1][-1]["y"]
    accepted = over_time[2][-1]["y"]
    assert found == len(
        [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability.state.status != VulnerabilityStateStatus.DELETED
        ]
    )
    assert accepted == len(
        [
            vulnerability
            for vulnerability in vulnerabilities
            if (
                vulnerability.treatment
                and vulnerability.treatment.status
                in {
                    VulnerabilityTreatmentStatus.ACCEPTED,
                    VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                }
                and vulnerability.state.status == VulnerabilityStateStatus.OPEN
            )
        ]
    )
    assert closed == len(
        [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability.state.status == VulnerabilityStateStatus.CLOSED
        ]
    )

    test_imamura_data: GroupUnreliableIndicators = (
        await loaders.group_indicators_typed.load("deleteimamura")
    )
    assert len(test_imamura_data) == 27


@pytest.mark.changes_db
@freeze_time("2022-04-20")
async def test_update_portfolios_indicators() -> None:
    loaders: Dataloaders = get_new_context()
    org_name = "okada"
    expected_tags = [
        "another-tag",
        "test-groups",
        "test-tag",
        "test-updates",
    ]
    org_tags = await loaders.organization_tags.load(org_name)
    org_tags_names = sorted([tag["tag"] for tag in org_tags])
    assert org_tags_names == expected_tags

    await update_portfolios.main()

    updated_tags = [
        "another-tag",
        "test-groups",
    ]
    loaders.organization_tags.clear(org_name)
    org_tags = await loaders.organization_tags.load(org_name)
    org_tags_names = sorted([tag["tag"] for tag in org_tags])
    assert org_tags_names == updated_tags

    tag_test_groups = next(
        tag for tag in org_tags if tag["tag"] == "test-groups"
    )
    assert tag_test_groups["last_closing_date"] == Decimal("946.0")
    assert tag_test_groups["max_open_severity"] == Decimal("6.3")
    assert tag_test_groups["max_severity"] == Decimal("6.3")
    assert tag_test_groups["mean_remediate"] == Decimal("687.0")
    assert tag_test_groups["mean_remediate_critical_severity"] == Decimal(
        "0.0"
    )
    assert tag_test_groups["mean_remediate_high_severity"] == Decimal("0.0")
    assert tag_test_groups["mean_remediate_low_severity"] == Decimal("692.0")
    assert tag_test_groups["mean_remediate_medium_severity"] == Decimal(
        "374.0"
    )


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
    loaders: Dataloaders = get_new_context()
    test_group_name_1 = "setpendingdeletion"
    test_group_name_2 = "deletegroup"
    all_active_groups = await orgs_domain.get_all_active_groups_typed(loaders)
    all_active_groups_names = [group.name for group in all_active_groups]
    assert len(all_active_groups_names) == 14
    assert test_group_name_1 in all_active_groups_names
    assert test_group_name_2 in all_active_groups_names

    await delete_obsolete_groups.main()

    all_active_groups = await orgs_domain.get_all_active_groups_typed(loaders)
    all_active_groups_names = [group.name for group in all_active_groups]
    assert len(all_active_groups_names) == 13
    assert test_group_name_1 in all_active_groups_names
    assert test_group_name_2 not in all_active_groups_names

    loaders.group_typed.clear_all()
    test_group_1: Group = await loaders.group_typed.load(test_group_name_1)
    assert test_group_1.state.status == GroupStateStatus.ACTIVE
    assert test_group_1.state.pending_deletion_date

    test_group_2: Group = await loaders.group_typed.load(test_group_name_2)
    assert test_group_2.state.status == GroupStateStatus.DELETED
