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
from charts.generators.stacked_bar_chart.utils import (
    AssignedFormatted,
    format_stacked_percentages,
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
from typing import (
    Any,
    Counter,
    Dict,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> dict[str, List[Vulnerability]]:
    loaders: Dataloaders = get_new_context()
    assigned: Dict[str, List[Vulnerability]] = defaultdict(list)
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = tuple(finding.id for finding in group_findings)
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        finding_ids
    )

    for vulnerability in vulnerabilities:
        if vulnerability.treatment and vulnerability.treatment.assigned:
            assigned[vulnerability.treatment.assigned].append(vulnerability)

    return assigned


async def get_data_many_groups(
    groups: List[str],
) -> dict[str, List[Vulnerability]]:
    groups_data: Tuple[dict[str, List[Vulnerability]], ...] = await collect(
        map(get_data_one_group, groups), workers=32
    )
    assigned: dict[str, List[Vulnerability]] = defaultdict(list)

    for group in groups_data:
        for user, vulnerabilities in group.items():
            assigned[user].extend(vulnerabilities)

    return assigned


def format_assigned(
    user: str, vulnerabilities: List[Vulnerability]
) -> AssignedFormatted:
    status: Counter[str] = Counter(
        vulnerability.treatment.status for vulnerability in vulnerabilities
    )

    treatment: Counter[str] = Counter(
        vulnerability.treatment.status
        for vulnerability in vulnerabilities
        if vulnerability.state.status == VulnerabilityStateStatus.OPEN
        and vulnerability.treatment.status
        in {
            VulnerabilityTreatmentStatus.ACCEPTED,
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
        }
    )

    return AssignedFormatted(
        accepted=treatment[VulnerabilityTreatmentStatus.ACCEPTED],
        accepted_undefined=treatment[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        closed_vulnerabilities=status[VulnerabilityStateStatus.CLOSED],
        open_vulnerabilities=status[VulnerabilityStateStatus.OPEN],
        remaining_open_vulnerabilities=(
            status[VulnerabilityStateStatus.OPEN]
            - treatment[VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED]
            - treatment[VulnerabilityTreatmentStatus.ACCEPTED]
        ),
        user=user,
    )


def format_data(
    assigned_data: dict[str, List[Vulnerability]], limit: int = 20
) -> Dict[str, Any]:
    data: Tuple[AssignedFormatted, ...] = tuple(
        format_assigned(user, vulnerabilities)
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
    percentage_values = [
        format_stacked_percentages(
            values={
                "Closed": Decimal(group.closed_vulnerabilities),
                "Temporarily accepted": Decimal(group.accepted),
                "Permanently accepted": Decimal(group.accepted_undefined),
                "Open": Decimal(group.remaining_open_vulnerabilities),
            }
        )
        for group in limited_data
    ]

    return dict(
        data=dict(
            columns=[
                ["Closed"]
                + [
                    str(group.closed_vulnerabilities) for group in limited_data
                ],
                ["Temporarily accepted"]
                + [str(group.accepted) for group in limited_data],
                ["Permanently accepted"]
                + [str(group.accepted_undefined) for group in limited_data],
                ["Open"]
                + [
                    str(group.remaining_open_vulnerabilities)
                    for group in limited_data
                ],
            ],
            colors={
                "Closed": RISK.more_passive,
                "Temporarily accepted": TREATMENT.passive,
                "Permanently accepted": TREATMENT.more_passive,
                "Open": RISK.more_agressive,
            },
            labels=dict(
                format=dict(
                    Closed=None,
                ),
            ),
            type="bar",
            groups=[
                [
                    "Closed",
                    "Temporarily accepted",
                    "Permanently accepted",
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
        axis=dict(
            x=dict(
                categories=[group.user for group in limited_data],
                type="category",
                tick=dict(rotate=utils.TICK_ROTATION, multiline=False),
            ),
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        percentageValues={
            "Closed": [
                percentage_value[0]["Closed"]
                for percentage_value in percentage_values
            ],
            "Temporarily accepted": [
                percentage_value[0]["Temporarily accepted"]
                for percentage_value in percentage_values
            ],
            "Permanently accepted": [
                percentage_value[0]["Permanently accepted"]
                for percentage_value in percentage_values
            ],
            "Open": [
                percentage_value[0]["Open"]
                for percentage_value in percentage_values
            ],
        },
        maxPercentageValues={
            "Closed": [
                percentage_value[1]["Closed"]
                for percentage_value in percentage_values
            ],
            "Temporarily accepted": [
                percentage_value[1]["Temporarily accepted"]
                for percentage_value in percentage_values
            ],
            "Permanently accepted": [
                percentage_value[1]["Permanently accepted"]
                for percentage_value in percentage_values
            ],
            "Open": [
                percentage_value[1]["Open"]
                for percentage_value in percentage_values
            ],
        },
    )


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                assigned_data=await get_data_one_group(group),
                limit=18,
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                assigned_data=await get_data_many_groups(list(org_groups)),
                limit=18,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    assigned_data=await get_data_many_groups(groups),
                    limit=18,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
