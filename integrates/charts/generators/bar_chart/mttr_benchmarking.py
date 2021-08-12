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
from charts.colors import (
    RISK,
)
from custom_types import (
    Vulnerability,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from groups.domain import (
    get_mean_remediate,
)
from statistics import (
    mean,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Tuple,
)


class OrganizationBenchmarking(NamedTuple):
    is_valid: bool
    mttr: Decimal
    organization_id: str


def get_vulnerability_reattacks(*, vulnerability: Vulnerability) -> int:
    return sum(
        1
        for verification in vulnerability["historic_verification"]
        if verification.get("status") == "REQUESTED"
    )


@alru_cache(maxsize=None, typed=True)
async def get_group_reattacks(*, group: str, loaders: Dataloaders) -> int:
    group_findings = await loaders.group_findings.load(group)
    vulnerabilities = await loaders.finding_vulns.load_many_chained(
        [str(finding["finding_id"]) for finding in group_findings]
    )

    return sum(
        get_vulnerability_reattacks(vulnerability=vulnerability)
        for vulnerability in vulnerabilities
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_organization(
    *, organization_id: str, groups: Tuple[str, ...], loaders: Dataloaders
) -> OrganizationBenchmarking:
    groups_mttr_data = await collect(
        [get_mean_remediate(loaders, group.lower()) for group in groups],
        workers=12,
    )
    groups_reattacks_data = await collect(
        [
            get_group_reattacks(group=group.lower(), loaders=loaders)
            for group in groups
        ],
        workers=12,
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
        organization_id=organization_id,
        mttr=mttr,
    )


def format_data(data: Tuple[Decimal, Decimal, Decimal]) -> Dict[str, Any]:

    return dict(
        data=dict(
            columns=[
                [
                    "Mean time to remediate",
                    Decimal("0") if data[0] == Decimal("0") else data[0],
                    data[1],
                    data[2],
                ]
            ],
            colors={
                "Mean time to remediate": RISK.neutral,
            },
            type="bar",
        ),
        axis=dict(
            x=dict(
                categories=[
                    "My organization",
                    "Average all organizations",
                    "Best organization",
                ],
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartYTickFormat=True,
    )


def get_valid_organizations(
    *,
    organizations: Tuple[OrganizationBenchmarking, ...],
    organization_id: str,
) -> List[OrganizationBenchmarking]:
    return [
        organization
        for organization in organizations
        if organization_id != organization.organization_id
        and organization.is_valid
        and organization.mttr != Decimal("Infinity")
    ]


def get_mean_organizations(
    *, organizations: List[OrganizationBenchmarking]
) -> Decimal:
    return (
        Decimal(
            mean([organization.mttr for organization in organizations])
        ).to_integral_exact(rounding=ROUND_CEILING)
        if organizations
        else Decimal("0")
    )


def get_best_mttr(*, organizations: List[OrganizationBenchmarking]) -> Decimal:
    return (
        Decimal(
            min([organization.mttr for organization in organizations])
        ).to_integral_exact(rounding=ROUND_CEILING)
        if organizations
        else Decimal("0")
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
                            organization_id=org_id,
                        )
                    ),
                    best_mttr,
                ),
            ),
            entity="organization",
            subject=org_id,
        )


if __name__ == "__main__":
    run(generate_all())
