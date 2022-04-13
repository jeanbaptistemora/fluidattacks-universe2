from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.stacked_bar_chart.utils import (
    AssignedFormatted,
    format_stacked_vulnerabilities_data,
)
from charts.utils import (
    get_cvssf,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from collections import (
    defaultdict,
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
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from typing import (
    Any,
    Counter,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> dict[str, List[Tuple[Vulnerability, Decimal]]]:
    assigned: dict[str, List[Tuple[Vulnerability, Decimal]]] = defaultdict(
        list
    )
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        tuple(finding.id for finding in group_findings)
    )
    finding_cvssf: dict[str, Decimal] = {
        finding.id: get_cvssf(get_severity_score(finding.severity))
        for finding in group_findings
    }

    for vulnerability in vulnerabilities:
        if vulnerability.treatment and vulnerability.treatment.assigned:
            assigned[vulnerability.treatment.assigned].append(
                (vulnerability, finding_cvssf[vulnerability.finding_id])
            )

    return assigned


async def get_data_many_groups(
    *,
    groups: Tuple[str, ...],
    loaders: Dataloaders,
) -> dict[str, List[Tuple[Vulnerability, Decimal]]]:
    groups_data: Tuple[
        dict[str, List[Tuple[Vulnerability, Decimal]]], ...
    ] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )
    assigned: dict[str, List[Tuple[Vulnerability, Decimal]]] = defaultdict(
        list
    )

    for group in groups_data:
        for user, vulnerabilities in group.items():
            assigned[user].extend(vulnerabilities)

    return assigned


def format_assigned(
    *, user: str, vulnerabilities: List[Tuple[Vulnerability, Decimal]]
) -> AssignedFormatted:
    status: Counter[str] = Counter()
    treatment: Counter[str] = Counter()

    for vulnerability, cvssf in vulnerabilities:
        status.update({vulnerability.state.status: cvssf})
        if (
            vulnerability.state.status == VulnerabilityStateStatus.OPEN
            and vulnerability.treatment.status
            in {
                VulnerabilityTreatmentStatus.ACCEPTED,
                VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
            }
        ):
            treatment.update({vulnerability.treatment.status: cvssf})

    remaining_open: Decimal = Decimal(
        status[VulnerabilityStateStatus.OPEN]
        - treatment[VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED]
        - treatment[VulnerabilityTreatmentStatus.ACCEPTED]
    )

    return AssignedFormatted(
        accepted=treatment[VulnerabilityTreatmentStatus.ACCEPTED],
        accepted_undefined=treatment[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        closed_vulnerabilities=status[VulnerabilityStateStatus.CLOSED],
        open_vulnerabilities=status[VulnerabilityStateStatus.OPEN],
        remaining_open_vulnerabilities=remaining_open
        if remaining_open > Decimal("0.0")
        else Decimal("0.0"),
        user=user,
    )


def format_data(
    *, assigned_data: dict[str, List[Tuple[Vulnerability, Decimal]]]
) -> dict[str, Any]:
    limit: int = 18
    data: Tuple[AssignedFormatted, ...] = tuple(
        format_assigned(user=user, vulnerabilities=vulnerabilities)
        for user, vulnerabilities in assigned_data.items()
    )
    limited_data = list(
        sorted(
            data,
            key=lambda x: (
                x.open_vulnerabilities
                / (x.closed_vulnerabilities + x.open_vulnerabilities)
                if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
                else 0
            ),
            reverse=True,
        )
    )[:limit]

    return format_stacked_vulnerabilities_data(limited_data=limited_data)


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for group in iterate_groups():
        json_dump(
            document=format_data(
                assigned_data=await get_data_one_group(
                    group=group, loaders=loaders
                ),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_data(
                assigned_data=await get_data_many_groups(
                    groups=org_groups, loaders=loaders
                ),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    assigned_data=await get_data_many_groups(
                        groups=tuple(groups), loaders=loaders
                    ),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
