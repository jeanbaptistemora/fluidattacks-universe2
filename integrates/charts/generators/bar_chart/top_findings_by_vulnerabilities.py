# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    format_data_csv,
    generate_all_top_vulnerabilities,
    LIMIT,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.common.colors import (
    VULNERABILITIES_COUNT,
)
from charts.generators.common.utils import (
    get_finding_name,
)
from charts.utils import (
    CsvData,
)
from dataloaders import (
    Dataloaders,
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
)
from itertools import (
    groupby,
)
from typing import (
    Counter,
    Union,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str, loaders: Dataloaders) -> Counter[str]:
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    finding_vulns: tuple[
        tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many(finding_ids)
    counter = Counter(
        [
            f"{finding.id}/{finding.title}"
            for finding, vulnerabilities in zip(group_findings, finding_vulns)
            for vulnerability in vulnerabilities
            if vulnerability.state.status == VulnerabilityStateStatus.OPEN
        ]
    )

    return counter


async def get_data_many_groups(
    groups: list[str], loaders: Dataloaders
) -> Counter[str]:
    groups_data: tuple[Counter[str], ...] = await collect(
        tuple(get_data_one_group(group, loaders) for group in groups),
        workers=32,
    )
    return sum(groups_data, Counter())


def format_data(counters: Counter[str]) -> tuple[dict, CsvData]:
    data: list[tuple[str, int]] = counters.most_common()
    merged_data: list[list[Union[int, str]]] = []
    for axis, columns in groupby(
        sorted(data, key=lambda x: get_finding_name([x[0]])),
        key=lambda x: get_finding_name([x[0]]),
    ):
        merged_data.append([axis, sum([value for _, value in columns])])

    merged_data = sorted(merged_data, key=lambda x: x[1], reverse=True)
    limited_merged_data = merged_data[:LIMIT]

    json_data = dict(
        data=dict(
            columns=[
                [
                    "# Open Vulnerabilities",
                    *[value for _, value in limited_merged_data],
                ],
            ],
            colors={
                "# Open Vulnerabilities": VULNERABILITIES_COUNT,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        padding=dict(
            bottom=0,
        ),
        exposureTrendsByCategories=True,
        keepToltipColor=True,
        axis=dict(
            rotated=True,
            x=dict(
                categories=[
                    get_finding_name([str(key)])
                    for key, _ in limited_merged_data
                ],
                type="category",
                tick=dict(
                    outer=False,
                    rotate=0,
                ),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartYTickFormat=True,
        maxValue=format_max_value(
            [(key, Decimal(value)) for key, value in limited_merged_data]
        ),
    )
    csv_data = format_data_csv(
        header_value=json_data["data"]["columns"][0][0],
        values=[value for _, value in merged_data],
        categories=[group for group, _ in merged_data],
        header_title="Type",
    )

    return (json_data, csv_data)


if __name__ == "__main__":
    run(
        generate_all_top_vulnerabilities(
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            format_data=format_data,
        )
    )
