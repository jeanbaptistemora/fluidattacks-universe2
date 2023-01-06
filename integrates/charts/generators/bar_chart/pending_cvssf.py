from aioextensions import (
    collect,
    run,
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
    OTHER_COUNT,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from charts.generators.text_box.pending_cvssf import (
    generate_one,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from operator import (
    attrgetter,
)


async def get_data_many_groups(
    *,
    groups: tuple[str, ...],
    loaders: Dataloaders,
) -> list[PortfoliosGroupsInfo]:
    groups_data = await collect(
        tuple(generate_one(group, loaders) for group in groups),
        workers=2,
    )

    return sorted(groups_data, key=attrgetter("value"), reverse=True)


def format_data(
    data: list[PortfoliosGroupsInfo],
) -> tuple[dict, utils.CsvData]:
    limited_data = [group for group in data[:LIMIT] if group.value > 0]

    json_data: dict = dict(
        data=dict(
            columns=[
                ["Pending CVSSF"]
                + [
                    str(utils.format_cvssf_log(group.value))
                    for group in limited_data
                ],
            ],
            colors={
                "Pending CVSSF": OTHER_COUNT,
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
                categories=[group.group_name for group in limited_data],
                type="category",
                tick=dict(
                    multiline=False,
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
            [
                (group.group_name, utils.format_cvssf(group.value))
                for group in limited_data
            ]
        ),
        maxValueLog=format_max_value(
            [
                (group.group_name, utils.format_cvssf_log(group.value))
                for group in limited_data
            ]
        ),
        originalValues=[
            utils.format_cvssf(group.value) for group in limited_data
        ],
        exposureTrendsByCategories=True,
        keepToltipColor=True,
    )

    csv_data = format_data_csv(
        header_value=str(json_data["data"]["columns"][0][0]),
        values=[utils.format_cvssf(group.value) for group in data],
        categories=[group.group_name for group in data],
    )

    return (json_data, csv_data)


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        json_document, csv_document = format_data(
            data=await get_data_many_groups(groups=org_groups, loaders=loaders)
        )
        utils.json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            json_document, csv_document = format_data(
                data=await get_data_many_groups(
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
