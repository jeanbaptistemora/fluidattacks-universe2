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
    Benchmarking,
    format_data,
    get_best_mttr,
    get_mean_organizations,
    get_valid_subjects,
    get_vulnerability_reattacks,
    GROUP_CATEGORIES,
    ORGANIZATION_CATEGORIES,
    PORTFOLIO_CATEGORIES,
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
    get_alive_group_names,
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
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> Benchmarking:
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

    number_of_reattacks: int = sum(
        get_vulnerability_reattacks(vulnerability=vulnerability)
        for vulnerability in vulnerabilities_excluding_permanently_accepted
    )

    if FI_API_STATUS == "migration":
        mttr: Decimal = await get_mean_remediate_non_treated_new(
            loaders, group.lower()
        )
    else:
        mttr = await get_mean_remediate_non_treated(loaders, group.lower())

    return Benchmarking(
        is_valid=number_of_reattacks > 10,
        subject=group.lower(),
        mttr=mttr,
        number_of_reattacks=number_of_reattacks,
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_organization(
    *, organization_id: str, groups: Tuple[str, ...], loaders: Dataloaders
) -> Benchmarking:
    groups_data: Tuple[Benchmarking, ...] = await collect(
        [get_data_one_group(group=group, loaders=loaders) for group in groups]
    )

    mttr: Decimal = (
        Decimal(
            mean([group_data.mttr for group_data in groups_data])
        ).to_integral_exact(rounding=ROUND_CEILING)
        if groups_data
        else Decimal("Infinity")
    )
    number_of_reattacks = sum(
        group_data.number_of_reattacks for group_data in groups_data
    )

    return Benchmarking(
        is_valid=number_of_reattacks > 1000,
        subject=organization_id,
        mttr=mttr,
        number_of_reattacks=number_of_reattacks,
    )


async def generate_all() -> None:  # pylint: disable=too-many-locals
    loaders: Dataloaders = get_new_context()
    organizations: List[Tuple[str, Tuple[str, ...]]] = []
    portfolios: List[Tuple[str, Tuple[str, ...]]] = []
    groups: List[str] = list(
        sorted(await get_alive_group_names(), reverse=True)
    )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        organizations.append((org_id, org_groups))

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, p_groups in await utils.get_portfolios_groups(org_name):
            portfolios.append((portfolio, tuple(p_groups)))

    all_groups_data: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_one_group(
                group=group,
                loaders=loaders,
            )
            for group in groups
        ],
        workers=24,
    )

    all_organizations_data: Tuple[Benchmarking, ...] = await collect(
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

    all_portfolios_data: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_one_organization(
                organization_id=portfolio[0],
                groups=portfolio[1],
                loaders=loaders,
            )
            for portfolio in portfolios
        ],
        workers=24,
    )

    best_mttr = get_best_mttr(
        subjects=[
            organization
            for organization in all_organizations_data
            if organization.is_valid
        ]
    )

    best_group_mttr = get_best_mttr(
        subjects=[group for group in all_groups_data if group.is_valid]
    )

    best_portfolio_mttr = get_best_mttr(
        subjects=[
            portfolio
            for portfolio in all_portfolios_data
            if portfolio.is_valid
        ]
    )

    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                data=(
                    Decimal(
                        (
                            await get_data_one_group(
                                group=group,
                                loaders=loaders,
                            )
                        ).mttr
                    ).to_integral_exact(rounding=ROUND_CEILING),
                    get_mean_organizations(
                        organizations=get_valid_subjects(
                            all_subjects=all_groups_data,
                            subject=group,
                        )
                    ),
                    best_group_mttr,
                ),
                categories=GROUP_CATEGORIES,
            ),
            entity="group",
            subject=group,
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
                        organizations=get_valid_subjects(
                            all_subjects=all_organizations_data,
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

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    data=(
                        (
                            await get_data_one_organization(
                                organization_id=portfolio,
                                groups=tuple(groups),
                                loaders=loaders,
                            )
                        ).mttr,
                        get_mean_organizations(
                            organizations=get_valid_subjects(
                                all_subjects=all_portfolios_data,
                                subject=portfolio,
                            )
                        ),
                        best_portfolio_mttr,
                    ),
                    categories=PORTFOLIO_CATEGORIES,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
