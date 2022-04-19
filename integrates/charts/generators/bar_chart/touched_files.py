from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    RISK,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
    TICK_ROTATION,
)
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
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from newutils.datetime import (
    get_datetime_from_iso_str,
    get_now_minus_delta,
)
from typing import (
    Any,
    Counter,
    Dict,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders, date_minus_delta: datetime
) -> Counter[str]:
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        tuple(finding.id for finding in group_findings)
    )

    return Counter(
        tuple(
            vulnerability.where
            for vulnerability in vulnerabilities
            if get_datetime_from_iso_str(
                vulnerability.unreliable_indicators.unreliable_report_date
            )
            > date_minus_delta
            and vulnerability.type == VulnerabilityType.LINES
            and vulnerability.state.status == VulnerabilityStateStatus.OPEN
        )
    )


async def get_data_many_groups(
    *,
    groups: Tuple[str, ...],
    loaders: Dataloaders,
    date_minus_delta: datetime,
) -> Counter[str]:

    groups_data = await collect(
        tuple(
            get_data_one_group(
                group=group, loaders=loaders, date_minus_delta=date_minus_delta
            )
            for group in groups
        ),
        workers=32,
    )

    return sum(groups_data, Counter())


def format_data(*, counters: Counter[str]) -> Dict[str, Any]:
    merged_data: List[Tuple[str, int]] = counters.most_common()[:20]

    return dict(
        data=dict(
            columns=[
                [
                    "# Vulnerabilities",
                    *[value for _, value in merged_data],
                ],
            ],
            colors={
                "# Vulnerabilities": RISK.neutral,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            position="inset",
            inset=dict(
                anchor="top-right",
                step=1.25,
                x=10,
                y=-5,
            ),
        ),
        axis=dict(
            x=dict(
                categories=[key for key, _ in merged_data],
                type="category",
                tick=dict(
                    outer=False,
                    rotate=TICK_ROTATION,
                ),
            ),
            y=dict(
                label=dict(
                    text="# Vulnerabilities",
                    position="inner-top",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartXTickFormat=True,
        barChartYTickFormat=True,
        maxValue=format_max_value(
            [(key, Decimal(value)) for key, value in merged_data]
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    date_minus_delta: datetime = get_now_minus_delta(weeks=20)
    async for group in iterate_groups():
        json_dump(
            document=format_data(
                counters=await get_data_one_group(
                    group=group,
                    loaders=loaders,
                    date_minus_delta=date_minus_delta,
                ),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_data(
                counters=await get_data_many_groups(
                    groups=org_groups,
                    loaders=loaders,
                    date_minus_delta=date_minus_delta,
                ),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    counters=await get_data_many_groups(
                        groups=tuple(groups),
                        loaders=loaders,
                        date_minus_delta=date_minus_delta,
                    ),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
