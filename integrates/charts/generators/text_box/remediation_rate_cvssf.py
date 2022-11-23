from aioextensions import (
    run,
)
from charts.generators.stacked_bar_chart.cvssf_benchmarking import (
    get_data_one_organization,
    get_group_data,
    GroupBenchmarking,
    OrganizationCvssfBenchmarking,
)
from charts.generators.stacked_bar_chart.utils import (
    get_percentage,
)
from charts.generators.text_box.utils import (
    format_csv_data,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decimal import (
    Decimal,
)


def format_data(*, closed: Decimal) -> dict:

    return dict(
        fontSizeRatio=0.5,
        text=closed,
        percentage=True,
    )


async def generate_all() -> None:
    title: str = "Remediation Rate"
    total: Decimal
    values: list[Decimal]
    loaders: Dataloaders = get_new_context()
    async for group in iterate_groups():
        data_group: GroupBenchmarking = await get_group_data(
            group=group, loaders=loaders
        )
        total = (
            Decimal(
                data_group.counter["closed"]
                + data_group.counter["accepted"]
                + data_group.counter["open"]
            )
            if data_group.counter["total"] > Decimal("0.0")
            else Decimal("0.1")
        )
        values = [
            data_group.counter["closed"] / total,
            data_group.counter["accepted"] / total,
            data_group.counter["open"] / total,
        ]
        percentages = get_percentage(values)
        document = format_data(
            closed=percentages[0],
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                header=title, value=str(document["text"])
            ),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        data: OrganizationCvssfBenchmarking = await get_data_one_organization(
            organization_id=org_id, groups=org_groups, loaders=loaders
        )
        total = (
            Decimal(data.closed + data.accepted + data.open)
            if data.total > Decimal("0.0")
            else Decimal("0.1")
        )
        values = [
            data.closed / total,
            data.accepted / total,
            data.open / total,
        ]
        percentages = get_percentage(values)
        document = format_data(
            closed=percentages[0],
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                header=title, value=str(document["text"])
            ),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            data = await get_data_one_organization(
                organization_id=f"{org_id}PORTFOLIO#{portfolio}",
                groups=groups,
                loaders=loaders,
            )
            total = (
                Decimal(data.closed + data.accepted + data.open)
                if data.total > Decimal("0.0")
                else Decimal("0.1")
            )
            values = [
                data.closed / total,
                data.accepted / total,
                data.open / total,
            ]
            percentages = get_percentage(values)
            document = format_data(
                closed=percentages[0],
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    header=title, value=str(document["text"])
                ),
            )


if __name__ == "__main__":
    run(generate_all())
