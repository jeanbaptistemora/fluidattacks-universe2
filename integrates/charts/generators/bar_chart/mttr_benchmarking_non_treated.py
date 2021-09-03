from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts import (
    utils,
)
from charts.generators.bar_chart.utils import (
    format_data,
    get_best_mttr,
    get_mean_organizations,
    get_valid_organizations,
    get_vulnerability_reattacks,
    ORGANIZATION_CATEGORIES,
    OrganizationBenchmarking,
)
from context import (
    FI_API_STATUS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from groups.domain import (
    get_mean_remediate_non_treated,
    get_mean_remediate_non_treated_new,
)
from newutils.vulnerabilities import (
    filter_non_confirmed_zero_risk,
    is_accepted_undefined_vulnerability,
)
from statistics import (
    mean,
)
from typing import (
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_group_reattacks(*, group: str, loaders: Dataloaders) -> int:
    if FI_API_STATUS == "migration":
        group_findings_new: Tuple[
            Finding, ...
        ] = await loaders.group_findings_new.load(group.lower())
        all_vulnerabilities = await loaders.finding_vulns.load_many_chained(
            [finding.id for finding in group_findings_new]
        )
    else:
        group_findings = await loaders.group_findings.load(group)
        all_vulnerabilities = await loaders.finding_vulns.load_many_chained(
            [str(finding["finding_id"]) for finding in group_findings]
        )

    vulnerabilities = filter_non_confirmed_zero_risk(all_vulnerabilities)
    vulnerabilities_excluding_permanently_accepted = [
        vulnerability
        for vulnerability in vulnerabilities
        if not is_accepted_undefined_vulnerability(vulnerability)
    ]

    return sum(
        get_vulnerability_reattacks(vulnerability=vulnerability)
        for vulnerability in vulnerabilities_excluding_permanently_accepted
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_organization(
    *, organization_id: str, groups: Tuple[str, ...], loaders: Dataloaders
) -> OrganizationBenchmarking:
    if FI_API_STATUS == "migration":
        groups_mttr_data = await collect(
            [
                get_mean_remediate_non_treated_new(loaders, group.lower())
                for group in groups
            ],
            workers=24,
        )
    else:
        groups_mttr_data = await collect(
            [
                get_mean_remediate_non_treated(loaders, group.lower())
                for group in groups
            ],
            workers=24,
        )

    groups_reattacks_data = await collect(
        [
            get_group_reattacks(group=group.lower(), loaders=loaders)
            for group in groups
        ],
        workers=24,
    )

    mttr: Decimal = (
        Decimal(mean(groups_mttr_data)).to_integral_exact(
            rounding=ROUND_CEILING
        )
        if groups_mttr_data
        else Decimal("Infinity")
    )

    return OrganizationBenchmarking(
        is_valid=sum(groups_reattacks_data) > 1000,
        subject=organization_id,
        mttr=mttr,
        number_of_reattacks=sum(groups_reattacks_data),
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    organizations: List[Tuple[str, Tuple[str, ...]]] = []

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        organizations.append((org_id, org_groups))

    all_organizations_data = await collect(
        [
            get_data_one_organization(
                organization_id=organization[0],
                groups=organization[1],
                loaders=loaders,
            )
            for organization in organizations
        ],
        workers=24,
    )

    best_mttr = get_best_mttr(
        organizations=[
            organization
            for organization in all_organizations_data
            if organization.is_valid
        ]
    )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=(
                    (
                        await get_data_one_organization(
                            organization_id=org_id,
                            groups=org_groups,
                            loaders=loaders,
                        )
                    ).mttr,
                    get_mean_organizations(
                        organizations=get_valid_organizations(
                            organizations=all_organizations_data,
                            subject=org_id,
                        )
                    ),
                    best_mttr,
                ),
                categories=ORGANIZATION_CATEGORIES,
            ),
            entity="organization",
            subject=org_id,
        )


if __name__ == "__main__":
    run(generate_all())
