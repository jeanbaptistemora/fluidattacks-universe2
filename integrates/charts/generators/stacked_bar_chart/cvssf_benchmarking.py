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
    ROUND_FLOOR,
)
from findings.domain import (
    get_severity_score_new,
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
    if FI_API_STATUS == "migration":
        group_findings_new: Tuple[
            Finding, ...
        ] = await loaders.group_findings_new.load(group.lower())
        finding_severity.update(
            {
                finding.id: get_severity_score_new(finding.severity)
                for finding in group_findings_new
            }
        )
        vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
            [finding.id for finding in group_findings_new]
        )
    else:
        group_findings = await loaders.group_findings.load(group)
        finding_severity.update(
            {
                str(finding["finding_id"]): Decimal(
                    finding.get("cvss_temporal", "0.0")
                ).quantize(Decimal("0.1"))
                for finding in group_findings
            }
        )
        vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
            [str(finding["finding_id"]) for finding in group_findings]
        )

    counter: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        severity: Decimal = utils.get_cvssf(
            finding_severity[str(vulnerability["finding_id"])]
        )
        counter.update({"total": severity})
        if vulnerability["current_state"] == "open":
            if vulnerability["historic_treatment"][-1]["treatment"] in {
                "ACCEPTED",
                "ACCEPTED_UNDEFINED",
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
        [
            get_group_data(group=group.lower(), loaders=loaders)
            for group in groups
        ],
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


def round_percentage(percentages: List[Decimal], last: int) -> List[Decimal]:
    sum_percentage = sum(percentages)
    if sum_percentage == Decimal("100.0") or sum_percentage == Decimal("0.0"):
        return percentages

    if last < 0:
        return percentages

    new_percentages = [
        percentage + Decimal("1.0") if index == last else percentage
        for index, percentage in enumerate(percentages)
    ]
    return round_percentage(new_percentages, last - 1)


def get_percentage(values: List[Decimal]) -> List[Decimal]:
    percentages = [
        Decimal(value * Decimal("100.0")).to_integral_exact(
            rounding=ROUND_FLOOR
        )
        for value in values
    ]
    return round_percentage(percentages, len(percentages) - 1)


def format_data(
    *,
    organization: OrganizationCvssfBenchmarking,
    best_cvssf: OrganizationCvssfBenchmarking,
    mean_cvssf: OrganizationCvssfBenchmarking,
    worst_cvssf: OrganizationCvssfBenchmarking,
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
    max_organization = max(my_organization) if max(my_organization) else ""
    max_best = max(best_organization) if max(best_organization) else ""
    max_average = (
        max(average_organization) if max(average_organization) else ""
    )
    max_worst = max(worst_organization) if max(worst_organization) else ""

    max_percentage_values = dict(
        Closed=[
            my_organization[0]
            if my_organization[0] == max_organization
            else "",
            best_organization[0] if best_organization[0] == max_best else "",
            average_organization[0]
            if average_organization[0] == max_average
            else "",
            worst_organization[0]
            if worst_organization[0] == max_worst
            else "",
        ],
        Accepted=[
            my_organization[1]
            if my_organization[1] == max_organization
            else "",
            best_organization[1] if best_organization[1] == max_best else "",
            average_organization[1]
            if average_organization[1] == max_average
            else "",
            worst_organization[1]
            if worst_organization[1] == max_worst
            else "",
        ],
        Open=[
            my_organization[2]
            if my_organization[2] == max_organization
            else "",
            best_organization[2] if best_organization[2] == max_best else "",
            average_organization[2]
            if average_organization[2] == max_average
            else "",
            worst_organization[2]
            if worst_organization[2] == max_worst
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
                categories=[
                    "My organization",
                    "Best organization",
                    "Average organization",
                    "Worst organization",
                ],
                type="category",
                tick=dict(multiline=False),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                label=dict(
                    text="Severity (CVSSF)",
                    position="inner-top",
                ),
            ),
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        normalizedToolTip=True,
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

    best_cvssf = get_best_organization(organizations=all_organizations_data)
    worst_cvssf = get_worst_organization(organizations=all_organizations_data)

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
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
            ),
            entity="organization",
            subject=org_id,
        )


if __name__ == "__main__":
    run(generate_all())
