from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    format_data_csv,
    LIMIT,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.common.colors import (
    VULNERABILITIES_COUNT,
)
from charts.utils import (
    CsvData,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
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
    get_now_minus_delta,
)
import re
from typing import (
    Counter,
)


def format_where(where: str) -> str:
    # filename (package) [CVE]
    if match := re.match(r"(?P<where>.*)\s\(.*\)\s\[.*\]", where):
        return match.groupdict()["where"]

    return where


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders, date_minus_delta: datetime
) -> Counter[str]:
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
        [finding.id for finding in group_findings]
    )

    return Counter(
        tuple(
            format_where(vulnerability.state.where)
            for vulnerability in vulnerabilities
            if vulnerability.created_date > date_minus_delta
            and vulnerability.type == VulnerabilityType.LINES
            and vulnerability.state.status
            == VulnerabilityStateStatus.VULNERABLE
        )
    )


async def get_data_many_groups(
    *,
    groups: tuple[str, ...],
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


def format_data(*, counters: Counter[str]) -> tuple[dict, CsvData]:
    merged_data: list[tuple[str, int]] = counters.most_common()
    limited_merged_data = merged_data[:LIMIT]

    json_data = dict(
        data=dict(
            columns=[
                [
                    "# Vulnerabilities",
                    *[value for _, value in limited_merged_data],
                ],
            ],
            colors={
                "# Vulnerabilities": VULNERABILITIES_COUNT,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        axis=dict(
            rotated=True,
            x=dict(
                categories=[key for key, _ in limited_merged_data],
                type="category",
                tick=dict(
                    multiline=False,
                    outer=False,
                    rotate=0,
                ),
            ),
            y=dict(
                label=dict(
                    position="outer-top",
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
            [(key, Decimal(value)) for key, value in limited_merged_data]
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        exposureTrendsByCategories=True,
        keepToltipColor=True,
    )
    csv_data = format_data_csv(
        header_value="Number of vulnerabilities",
        values=[Decimal(value) for _, value in merged_data],
        categories=[name for name, _ in merged_data],
        header_title="File path",
    )

    return (json_data, csv_data)


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    date_minus_delta: datetime = get_now_minus_delta(weeks=20)
    async for group in iterate_groups():
        json_document, csv_document = format_data(
            counters=await get_data_one_group(
                group=group,
                loaders=loaders,
                date_minus_delta=date_minus_delta,
            ),
        )
        json_dump(
            document=json_document,
            entity="group",
            subject=group,
            csv_document=csv_document,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_document, csv_document = format_data(
            counters=await get_data_many_groups(
                groups=org_groups,
                loaders=loaders,
                date_minus_delta=date_minus_delta,
            ),
        )
        json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_document, csv_document = format_data(
                counters=await get_data_many_groups(
                    groups=tuple(groups),
                    loaders=loaders,
                    date_minus_delta=date_minus_delta,
                ),
            )
            json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
