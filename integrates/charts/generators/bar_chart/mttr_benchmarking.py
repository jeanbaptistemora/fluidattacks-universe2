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
    GROUP_CATEGORIES,
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
    get_alive_group_names,
    get_mean_remediate,
    get_mean_remediate_new,
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
) -> OrganizationBenchmarking:
    if FI_API_STATUS == "migration":
        group_findings_new: Tuple[
            Finding, ...
        ] = await loaders.group_findings_new.load(group.lower())
        vulnerabilities = await loaders.finding_vulns.load_many_chained(
            [finding.id for finding in group_findings_new]
        )
    else:
        group_findings = await loaders.group_findings.load(group)
        vulnerabilities = await loaders.finding_vulns.load_many_chained(
            [str(finding["finding_id"]) for finding in group_findings]
        )

    number_of_reattacks: int = sum(
        get_vulnerability_reattacks(vulnerability=vulnerability)
        for vulnerability in vulnerabilities
    )

    if FI_API_STATUS == "migration":
        mttr: Decimal = await get_mean_remediate_new(loaders, group.lower())
    else:
        mttr = await get_mean_remediate(loaders, group.lower())

    return OrganizationBenchmarking(
        is_valid=number_of_reattacks > 10,
        subject=group.lower(),
        mttr=mttr,
        number_of_reattacks=number_of_reattacks,
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_organization(
    *, organization_id: str, groups: Tuple[str, ...], loaders: Dataloaders
) -> OrganizationBenchmarking:

    groups_data: Tuple[OrganizationBenchmarking, ...] = await collect(
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

    return OrganizationBenchmarking(
        is_valid=number_of_reattacks > 1000,
        subject=organization_id,
        mttr=mttr,
        number_of_reattacks=number_of_reattacks,
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    organizations: List[Tuple[str, Tuple[str, ...]]] = []
    groups: List[str] = sorted(await get_alive_group_names(), reverse=True)

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        organizations.append((org_id, org_groups))

    all_groups_data = await collect(
        [
            get_data_one_group(
                group=group,
                loaders=loaders,
            )
            for group in groups
        ],
        workers=24,
    )

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

    best_group_mttr = get_best_mttr(
        organizations=[group for group in all_groups_data if group.is_valid]
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
                        organizations=get_valid_organizations(
                            organizations=all_groups_data,
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
