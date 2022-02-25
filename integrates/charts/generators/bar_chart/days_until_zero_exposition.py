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
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
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
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
    Tuple,
)


class DaysUntilZeroExposition(NamedTuple):
    closing_as_fastest: Decimal
    closing_as_median: Decimal
    closing_as_average: Decimal


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group_name: str, loaders: Dataloaders
) -> DaysUntilZeroExposition:
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name.lower()
    )
    findings_ids: Tuple[str, ...] = tuple(
        finding.id for finding in group_findings
    )
    finding_vulns: Tuple[
        Tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many(findings_ids)

    counter: Decimal = Decimal("0.0")
    for finding, vulnerabilities in zip(group_findings, finding_vulns):
        for vulnerability in vulnerabilities:
            if vulnerability.state.status == VulnerabilityStateStatus.OPEN:
                if finding.min_time_to_remediate:
                    counter += Decimal(finding.min_time_to_remediate)
                else:
                    counter += Decimal("60.0")

    minutes_days: Decimal = Decimal("24.0") * Decimal("60.0")

    return DaysUntilZeroExposition(
        closing_as_fastest=Decimal(counter / minutes_days).to_integral_exact(
            rounding=ROUND_CEILING
        ),
        closing_as_median=Decimal("0.0"),
        closing_as_average=Decimal("0.0"),
    )


async def get_data_many_groups(
    groups: Tuple[str, ...], loaders: Dataloaders
) -> DaysUntilZeroExposition:

    groups_data: Tuple[DaysUntilZeroExposition, ...] = await collect(
        tuple(get_data_one_group(group, loaders) for group in groups),
        workers=32,
    )

    return DaysUntilZeroExposition(
        closing_as_fastest=Decimal(
            sum(group.closing_as_fastest for group in groups_data)
        ),
        closing_as_median=Decimal(
            sum(group.closing_as_median for group in groups_data)
        ),
        closing_as_average=Decimal(
            sum(group.closing_as_average for group in groups_data)
        ),
    )


def format_data(counters: DaysUntilZeroExposition) -> Dict[str, Any]:

    return dict(
        data=dict(
            columns=[
                [
                    "Days until zero exposition",
                    counters.closing_as_fastest,
                    counters.closing_as_median,
                    counters.closing_as_average,
                ],
            ],
            colors={
                "Days until zero exposition": RISK.more_agressive,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=[
                    "Closing as fastest",
                    "Closing as median",
                    "Closing as average",
                ],
                type="category",
                tick=dict(
                    outer=False,
                ),
            ),
            y=dict(
                label=dict(
                    text="CVSSF",
                    position="inner-top",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        maxValue=format_max_value(
            [
                ("", counters.closing_as_fastest),
                ("", counters.closing_as_median),
                ("", counters.closing_as_average),
            ]
        ),
    )


async def generate_all() -> None:

    loaders: Dataloaders = get_new_context()
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                counters=await get_data_one_group(group, loaders),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                counters=await get_data_many_groups(org_groups, loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    counters=await get_data_many_groups(
                        tuple(groups), loaders
                    ),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
