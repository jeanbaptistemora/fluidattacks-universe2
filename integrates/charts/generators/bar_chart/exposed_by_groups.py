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
from charts.generators.bar_chart.utils import (
    format_data_csv,
    LIMIT,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.common.colors import (
    EXPOSURE,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from operator import (
    attrgetter,
)
from typing import (
    Counter,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> PortfoliosGroupsInfo:
    group_findings = await loaders.group_findings.load(group.lower())
    finding_ids = [finding.id for finding in group_findings]
    finding_cvssf: dict[str, Decimal] = {
        finding.id: utils.get_cvssf(get_severity_score(finding.severity))
        for finding in group_findings
    }

    vulnerabilities = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            finding_ids
        )
    )

    counter: Counter[str] = Counter()
    for vulnerability in vulnerabilities:
        if vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE:
            counter.update(
                {
                    "open": Decimal(
                        finding_cvssf[vulnerability.finding_id]
                    ).quantize(Decimal("0.001"))
                }
            )

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=utils.format_cvssf(Decimal(counter["open"])),
    )


async def get_data_many_groups(
    *,
    groups: tuple[str, ...],
    loaders: Dataloaders,
) -> list[PortfoliosGroupsInfo]:
    groups_data = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )

    return sorted(groups_data, key=attrgetter("value"), reverse=True)


def format_data(
    all_data: list[PortfoliosGroupsInfo],
) -> tuple[dict, utils.CsvData]:
    data = [
        group for group in all_data[:LIMIT] if group.value > Decimal("0.0")
    ]

    json_data: dict = dict(
        data=dict(
            columns=[
                ["Open exposure"]
                + [str(utils.format_cvssf_log(group.value)) for group in data],
            ],
            colors={
                "Open exposure": EXPOSURE,
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
                categories=[group.group_name for group in data],
                type="category",
                tick=dict(
                    rotate=0,
                    multiline=False,
                ),
            ),
            y=dict(
                label=dict(
                    text="CVSSF",
                    position="outer-top",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        maxValue=format_max_value(
            [(group.group_name, Decimal(group.value)) for group in data]
        ),
        maxValueLog=format_max_value(
            [
                (
                    group.group_name,
                    utils.format_cvssf_log(Decimal(group.value)),
                )
                for group in data
            ]
        ),
        originalValues=[
            utils.format_cvssf(Decimal(value)) for _, value in data
        ],
        exposureTrendsByCategories=True,
        keepToltipColor=True,
    )
    csv_data = format_data_csv(
        header_value=str(json_data["data"]["columns"][0][0]),
        values=[utils.format_cvssf(group.value) for group in all_data],
        categories=[group.group_name for group in all_data],
    )

    return (json_data, csv_data)


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        json_document, csv_document = format_data(
            all_data=await get_data_many_groups(
                groups=org_groups, loaders=loaders
            ),
        )
        utils.json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            json_document, csv_document = format_data(
                all_data=await get_data_many_groups(
                    groups=tuple(groups), loaders=loaders
                ),
            )
            utils.json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
