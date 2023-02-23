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
    TYPES_COUNT,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from dataloaders import (
    get_new_context,
)
from decimal import (
    Decimal,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups import (
    domain as groups_domain,
)
from operator import (
    attrgetter,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> PortfoliosGroupsInfo:
    context = get_new_context()
    open_findings = await groups_domain.get_open_findings(
        context, group.lower()
    )

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=Decimal(open_findings),
    )


async def get_data_many_groups(
    groups: tuple[str, ...],
) -> list[PortfoliosGroupsInfo]:
    groups_data = await collect(map(get_data_one_group, groups), workers=16)

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
                ["Open Types of Vulnerabilities"]
                + [group.value for group in data],
            ],
            colors={
                "Open Types of Vulnerabilities": TYPES_COUNT,
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
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartYTickFormat=True,
        maxValue=format_max_value(
            [(group.group_name, group.value) for group in data]
        ),
        exposureTrendsByCategories=True,
        keepToltipColor=True,
    )

    csv_data = format_data_csv(
        header_value=str(json_data["data"]["columns"][0][0]),
        values=[group.value for group in all_data],
        categories=[group.group_name for group in all_data],
    )

    return (json_data, csv_data)


@utils.retry_on_exceptions(
    default_value=None,
    exceptions=(UnavailabilityError,),
    retry_times=5,
)
async def generate_all() -> None:
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        json_document, csv_document = format_data(
            all_data=await get_data_many_groups(org_groups),
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
                all_data=await get_data_many_groups(groups),
            )
            utils.json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
