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
from charts.colors import (
    RISK,
)
from charts.generators.bar_chart.utils import (
    format_csv_data,
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
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in group_findings]
    )

    return Counter(
        tuple(
            format_where(vulnerability.where)
            for vulnerability in vulnerabilities
            if get_datetime_from_iso_str(vulnerability.created_date)
            > date_minus_delta
            and vulnerability.type == VulnerabilityType.LINES
            and vulnerability.state.status == VulnerabilityStateStatus.OPEN
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


def format_data(*, counters: Counter[str]) -> dict:
    merged_data: list[tuple[str, int]] = counters.most_common()[:15]

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
                    multiline=False,
                    outer=False,
                    rotate=TICK_ROTATION,
                ),
            ),
            y=dict(
                label=dict(
                    text="Vulnerabilities",
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
    header: str = "File path"
    alternative: str = "Number of vulnerabilities"
    async for group in iterate_groups():
        document = format_data(
            counters=await get_data_one_group(
                group=group,
                loaders=loaders,
                date_minus_delta=date_minus_delta,
            ),
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                document=document, header=header, alternative=alternative
            ),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            counters=await get_data_many_groups(
                groups=org_groups,
                loaders=loaders,
                date_minus_delta=date_minus_delta,
            ),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                document=document, header=header, alternative=alternative
            ),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_data(
                counters=await get_data_many_groups(
                    groups=tuple(groups),
                    loaders=loaders,
                    date_minus_delta=date_minus_delta,
                ),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    document=document, header=header, alternative=alternative
                ),
            )


if __name__ == "__main__":
    run(generate_all())
