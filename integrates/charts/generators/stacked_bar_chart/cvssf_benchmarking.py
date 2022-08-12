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
    TREATMENT,
)
from charts.generators.bar_chart.utils import (
    ORGANIZATION_CATEGORIES,
    PORTFOLIO_CATEGORIES,
)
from charts.generators.stacked_bar_chart import (
    format_csv_data,
)
from charts.generators.stacked_bar_chart.utils import (
    get_percentage,
    MIN_PERCENTAGE,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_severity_score,
)
from statistics import (
    mean,
)
from typing import (
    Any,
    Counter,
    Dict,
    List,
    NamedTuple,
    Tuple,
)


class OrganizationCvssfBenchmarking(NamedTuple):
    accepted: Decimal
    closed: Decimal
    open: Decimal
    organization_id: str
    total: Decimal


@alru_cache(maxsize=None, typed=True)
async def get_group_data(*, group: str, loaders: Dataloaders) -> Counter[str]:
    finding_severity: Dict[str, Decimal] = {}
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_severity.update(
        {
            finding.id: get_severity_score(finding.severity)
            for finding in group_findings
        }
    )
    vulnerabilities = (
        await loaders.finding_vulnerabilities_nzr.load_many_chained(
            [finding.id for finding in group_findings]
        )
    )

    counter: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        severity: Decimal = utils.get_cvssf(
            finding_severity[str(vulnerability.finding_id)]
        )
        counter.update({"total": severity})
        if vulnerability.state.status == VulnerabilityStateStatus.OPEN:
            if vulnerability.treatment and vulnerability.treatment.status in {
                VulnerabilityTreatmentStatus.ACCEPTED,
                VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
            }:
                counter.update({"accepted": severity})
            else:
                counter.update({"open": severity})
        else:
            counter.update({"closed": severity})

    return counter


@alru_cache(maxsize=None, typed=True)
async def get_data_one_organization(
    *, organization_id: str, groups: Tuple[str, ...], loaders: Dataloaders
) -> OrganizationCvssfBenchmarking:
    groups_data = await collect(
        tuple(
            get_group_data(group=group.lower(), loaders=loaders)
            for group in groups
        ),
        workers=24,
    )

    counter: Counter[str] = sum(groups_data, Counter())

    return OrganizationCvssfBenchmarking(
        accepted=Decimal(counter["accepted"]).quantize(Decimal("0.1")),
        closed=Decimal(counter["closed"]).quantize(Decimal("0.1")),
        open=Decimal(counter["open"]).quantize(Decimal("0.1")),
        organization_id=organization_id,
        total=Decimal(counter["total"]).quantize(Decimal("0.1")),
    )


def get_best_organization(
    *, organizations: List[OrganizationCvssfBenchmarking]
) -> OrganizationCvssfBenchmarking:
    if organizations:
        return max(
            organizations,
            key=lambda organization: Decimal(
                organization.closed / organization.total
            ).quantize(Decimal("0.0001"))
            if organization.total > Decimal("0.0")
            else Decimal("0.0"),
        )

    return OrganizationCvssfBenchmarking(
        accepted=Decimal("0.0"),
        closed=Decimal("1.0"),
        open=Decimal("0.0"),
        organization_id="",
        total=Decimal("1.0"),
    )


def get_worst_organization(
    *, organizations: List[OrganizationCvssfBenchmarking]
) -> OrganizationCvssfBenchmarking:
    if organizations:
        return min(
            organizations,
            key=lambda organization: Decimal(
                organization.closed / organization.total
            ).quantize(Decimal("0.0001"))
            if organization.total > Decimal("0.0")
            else Decimal("1.0"),
        )

    return OrganizationCvssfBenchmarking(
        accepted=Decimal("0.0"),
        closed=Decimal("0.0"),
        open=Decimal("1.0"),
        organization_id="",
        total=Decimal("1.0"),
    )


def get_mean_organizations(
    *, organizations: List[OrganizationCvssfBenchmarking]
) -> OrganizationCvssfBenchmarking:
    if organizations:
        accepted = Decimal(
            mean([organization.accepted for organization in organizations])
        ).quantize(Decimal("0.1"))
        opened = Decimal(
            mean([organization.open for organization in organizations])
        ).quantize(Decimal("0.1"))
        closed = Decimal(
            mean([organization.closed for organization in organizations])
        ).quantize(Decimal("0.1"))

        return OrganizationCvssfBenchmarking(
            accepted=accepted,
            closed=closed,
            open=opened,
            organization_id="",
            total=accepted + closed + opened,
        )

    return OrganizationCvssfBenchmarking(
        accepted=Decimal("0.0"),
        closed=Decimal("0.0"),
        open=Decimal("0.0"),
        organization_id="",
        total=Decimal("0.0"),
    )


def get_valid_organizations(
    *,
    organizations: Tuple[OrganizationCvssfBenchmarking, ...],
    organization_id: str,
) -> List[OrganizationCvssfBenchmarking]:
    return [
        organization
        for organization in organizations
        if organization_id != organization.organization_id
    ]


def format_data(
    *,
    organization: OrganizationCvssfBenchmarking,
    best_cvssf: OrganizationCvssfBenchmarking,
    mean_cvssf: OrganizationCvssfBenchmarking,
    worst_cvssf: OrganizationCvssfBenchmarking,
    categories: List[str],
) -> Dict[str, Any]:
    total_bar: List[Decimal] = [
        (organization.closed + organization.accepted + organization.open)
        if organization.total > Decimal("0.0")
        else Decimal("0.1"),
        best_cvssf.closed + best_cvssf.accepted + best_cvssf.open,
        (mean_cvssf.closed + mean_cvssf.accepted + mean_cvssf.open)
        if mean_cvssf.total > Decimal("0.0")
        else Decimal("0.1"),
        worst_cvssf.closed + worst_cvssf.accepted + worst_cvssf.open,
    ]
    percentage_values: List[List[Decimal]] = [
        [
            organization.closed / total_bar[0],
            organization.accepted / total_bar[0],
            organization.open / total_bar[0],
        ],
        [
            best_cvssf.closed / total_bar[1],
            best_cvssf.accepted / total_bar[1],
            best_cvssf.open / total_bar[1],
        ],
        [
            mean_cvssf.closed / total_bar[2],
            mean_cvssf.accepted / total_bar[2],
            mean_cvssf.open / total_bar[2],
        ],
        [
            worst_cvssf.closed / total_bar[3],
            worst_cvssf.accepted / total_bar[3],
            worst_cvssf.open / total_bar[3],
        ],
    ]
    my_organization = get_percentage(percentage_values[0])
    best_organization = get_percentage(percentage_values[1])
    average_organization = get_percentage(percentage_values[2])
    worst_organization = get_percentage(percentage_values[3])

    max_percentage_values = dict(
        Closed=[
            my_organization[0] if my_organization[0] >= MIN_PERCENTAGE else "",
            best_organization[0]
            if best_organization[0] >= MIN_PERCENTAGE
            else "",
            average_organization[0]
            if average_organization[0] >= MIN_PERCENTAGE
            else "",
            worst_organization[0]
            if worst_organization[0] >= MIN_PERCENTAGE
            else "",
        ],
        Accepted=[
            my_organization[1] if my_organization[1] >= MIN_PERCENTAGE else "",
            best_organization[1]
            if best_organization[1] >= MIN_PERCENTAGE
            else "",
            average_organization[1]
            if average_organization[1] >= MIN_PERCENTAGE
            else "",
            worst_organization[1]
            if worst_organization[1] >= MIN_PERCENTAGE
            else "",
        ],
        Open=[
            my_organization[2] if my_organization[2] >= MIN_PERCENTAGE else "",
            best_organization[2]
            if best_organization[2] >= MIN_PERCENTAGE
            else "",
            average_organization[2]
            if average_organization[2] >= MIN_PERCENTAGE
            else "",
            worst_organization[2]
            if worst_organization[2] >= MIN_PERCENTAGE
            else "",
        ],
    )

    return dict(
        data=dict(
            columns=[
                [
                    "Closed",
                    organization.closed,
                    best_cvssf.closed,
                    mean_cvssf.closed,
                    worst_cvssf.closed,
                ],
                [
                    "Accepted",
                    organization.accepted,
                    best_cvssf.accepted,
                    mean_cvssf.accepted,
                    worst_cvssf.accepted,
                ],
                [
                    "Open",
                    organization.open,
                    best_cvssf.open,
                    mean_cvssf.open,
                    worst_cvssf.open,
                ],
            ],
            colors={
                "Closed": RISK.more_passive,
                "Accepted": TREATMENT.passive,
                "Open": RISK.more_agressive,
            },
            type="bar",
            labels=dict(
                format=dict(
                    Closed=None,
                ),
            ),
            groups=[
                [
                    "Closed",
                    "Accepted",
                    "Open",
                ],
            ],
            order=None,
            stack=dict(
                normalize=True,
            ),
        ),
        legend=dict(
            position="bottom",
        ),
        grid=dict(
            y=dict(
                show=True,
            ),
        ),
        axis=dict(
            x=dict(
                categories=categories,
                type="category",
                tick=dict(multiline=False),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                label=dict(
                    text="Exposure (CVSSF)",
                    position="inner-top",
                ),
            ),
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        totalBar=total_bar,
        percentageValues=dict(
            Closed=[
                my_organization[0],
                best_organization[0],
                average_organization[0],
                worst_organization[0],
            ],
            Accepted=[
                my_organization[1],
                best_organization[1],
                average_organization[1],
                worst_organization[1],
            ],
            Open=[
                my_organization[2],
                best_organization[2],
                average_organization[2],
                worst_organization[2],
            ],
        ),
        maxPercentageValues=max_percentage_values,
    )


async def generate_all() -> None:  # pylint: disable=too-many-locals
    loaders: Dataloaders = get_new_context()
    organizations: List[Tuple[str, Tuple[str, ...]]] = []
    portfolios: List[Tuple[str, Tuple[str, ...]]] = []

    async for org_id, org_name, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        organizations.append((org_id, org_groups))
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            portfolios.append((portfolio, tuple(groups)))

    all_organizations_data = await collect(
        tuple(
            get_data_one_organization(
                organization_id=organization[0],
                groups=organization[1],
                loaders=loaders,
            )
            for organization in organizations
        ),
        workers=32,
    )

    all_portfolios_data = await collect(
        tuple(
            get_data_one_organization(
                organization_id=portfolios[0],
                groups=portfolios[1],
                loaders=loaders,
            )
            for portfolios in portfolios
        ),
        workers=32,
    )

    best_cvssf = get_best_organization(organizations=all_organizations_data)
    worst_cvssf = get_worst_organization(organizations=all_organizations_data)
    best_portfolio_cvssf = get_best_organization(
        organizations=all_portfolios_data
    )
    worst_portfolio_cvssf = get_worst_organization(
        organizations=all_portfolios_data
    )

    header: str = "Categories"
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            organization=await get_data_one_organization(
                organization_id=org_id,
                groups=org_groups,
                loaders=loaders,
            ),
            best_cvssf=best_cvssf,
            mean_cvssf=get_mean_organizations(
                organizations=get_valid_organizations(
                    organizations=all_organizations_data,
                    organization_id=org_id,
                )
            ),
            worst_cvssf=worst_cvssf,
            categories=ORGANIZATION_CATEGORIES,
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_data(
                organization=await get_data_one_organization(
                    organization_id=portfolio,
                    groups=tuple(groups),
                    loaders=loaders,
                ),
                best_cvssf=best_portfolio_cvssf,
                mean_cvssf=get_mean_organizations(
                    organizations=get_valid_organizations(
                        organizations=all_portfolios_data,
                        organization_id=portfolio,
                    )
                ),
                worst_cvssf=worst_portfolio_cvssf,
                categories=PORTFOLIO_CATEGORIES,
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document, header=header),
            )


if __name__ == "__main__":
    run(generate_all())
