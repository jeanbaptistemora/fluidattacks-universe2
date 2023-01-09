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
from db_model.groups.types import (
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.portfolios.types import (
    Portfolio,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from decimal import (
    Decimal,
)
from freezegun import (
    freeze_time,
)
from newutils import (
    organizations as orgs_utils,
)
from organizations.domain import (
    iterate_organizations,
)
import pytest
from schedulers import (
    delete_obsolete_orgs,
    update_indicators,
    update_portfolios,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
@freeze_time("2022-04-20")
async def test_update_group_indicators() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "unittesting"
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    vulnerabilities = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )

    await update_indicators.main()

    test_data: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    assert len(test_data) == 29
    assert test_data.last_closed_vulnerability_days == 946
    assert test_data.last_closed_vulnerability_finding == "457497316"
    assert test_data.max_open_severity == Decimal("6.3")
    assert test_data.max_severity == Decimal("6.3")
    assert test_data.closed_vulnerabilities == 7
    assert test_data.open_vulnerabilities == 29
    assert test_data.open_findings == 5
    assert test_data.mean_remediate == Decimal("791")
    assert test_data.mean_remediate_critical_severity == Decimal("0")
    assert test_data.mean_remediate_high_severity == Decimal("0")
    assert test_data.mean_remediate_low_severity == Decimal("801")
    assert test_data.mean_remediate_medium_severity == Decimal("749")
    assert test_data.treatment_summary == GroupTreatmentSummary(
        accepted=2, accepted_undefined=1, in_progress=1, untreated=25
    )

    over_time = [
        element[-12:]
        for element in test_data.remediated_over_time  # type: ignore
    ]
    found = over_time[0][-1]["y"]
    closed = over_time[1][-1]["y"]
    accepted = over_time[2][-1]["y"]
    assert found == len(
        [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability.state.status
            not in {
                VulnerabilityStateStatus.DELETED,
                VulnerabilityStateStatus.MASKED,
            }
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
                and vulnerability.state.status
                == VulnerabilityStateStatus.VULNERABLE
            )
        ]
    )
    assert closed == len(
        [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability.state.status == VulnerabilityStateStatus.SAFE
        ]
    )

    test_imamura_data: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load("deleteimamura")
    )
    assert len(test_imamura_data) == 29


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
    org_tags: tuple[
        Portfolio, ...
    ] = await loaders.organization_portfolios.load(org_name)
    org_tags_names = sorted([tag.id for tag in org_tags])
    assert org_tags_names == expected_tags

    await update_portfolios.main()

    loaders = get_new_context()
    updated_tags = [
        "another-tag",
        "test-groups",
        "test-tag",
        "test-updates",
    ]
    org_tags = await loaders.organization_portfolios.load(org_name)
    org_tags_names = sorted([tag.id for tag in org_tags])
    assert org_tags_names == updated_tags

    tag_test_groups: Portfolio = next(
        tag for tag in org_tags if tag.id == "test-groups"
    )
    assert tag_test_groups.unreliable_indicators.last_closing_date == Decimal(
        "946.0"
    )
    assert tag_test_groups.unreliable_indicators.max_severity == Decimal("6.3")
    assert tag_test_groups.unreliable_indicators.max_open_severity == Decimal(
        "6.3"
    )
    assert tag_test_groups.unreliable_indicators.mean_remediate == Decimal(
        "688.0"
    )
    assert (
        tag_test_groups.unreliable_indicators.mean_remediate_critical_severity
        == Decimal("0.0")
    )
    assert (
        tag_test_groups.unreliable_indicators.mean_remediate_high_severity
        == Decimal("0.0")
    )
    assert (
        tag_test_groups.unreliable_indicators.mean_remediate_low_severity
        == Decimal("693.0")
    )
    assert (
        tag_test_groups.unreliable_indicators.mean_remediate_medium_severity
        == Decimal("374.5")
    )


@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_delete_obsolete_orgs() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#d32674a9-9838-4337-b222-68c88bf54647"
    org_ids = []
    async for organization in iterate_organizations():
        if not orgs_utils.is_deleted(organization):
            org_ids.append(organization.id)
    assert org_id in org_ids
    assert len(org_ids) == 10

    await delete_obsolete_orgs.main()

    new_org_ids = []
    async for organization in iterate_organizations():
        new_org: Organization = await loaders.organization.load(
            organization.id
        )
        if not orgs_utils.is_deleted(new_org):
            new_org_ids.append(organization.id)
    assert org_id not in new_org_ids
    assert len(new_org_ids) == 9

    loaders = get_new_context()
    org_id = "ORG#ffddc7a3-7f05-4fc7-b65d-7defffa883c2"
    test_org: Organization = await loaders.organization.load(org_id)
    org_pending_deletion_date = test_org.state.pending_deletion_date
    assert org_pending_deletion_date
    assert org_pending_deletion_date == datetime.fromisoformat(
        "2020-01-30T00:00:00+00:00"
    )

    org_name = "okada"
    test_org = await loaders.organization.load(org_name)
    org_pending_deletion_date = test_org.state.pending_deletion_date
    assert org_pending_deletion_date is None
