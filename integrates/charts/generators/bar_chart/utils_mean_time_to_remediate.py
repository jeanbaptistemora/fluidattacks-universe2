from charts import (
    utils,
)
from charts.generators.bar_chart.utils import (
    format_csv_data,
    Remediate,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.common.utils import (
    BAR_RATIO_WIDTH,
    get_max_axis,
)
from collections.abc import (
    Awaitable,
    Callable,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
)


async def generate_all(  # pylint: disable=too-many-locals
    *,
    format_data: Callable[[Remediate], dict[str, Any]],
    get_data_one_group: Callable[
        [str, Dataloaders, date | None], Awaitable[Remediate]
    ],
    get_data_many_groups: Callable[
        [tuple[str, ...], Dataloaders, date | None], Awaitable[Remediate]
    ],
    alternative: str = "Mean time to remediate",
) -> None:
    loaders: Dataloaders = get_new_context()
    list_days: list[int] = [30, 90]
    dates: list[date] = [
        datetime_utils.get_now_minus_delta(days=list_days[0]).date(),
        datetime_utils.get_now_minus_delta(days=list_days[1]).date(),
    ]
    header: str = "Categories"
    for days, min_date in zip([None, *list_days], [None, *dates]):
        async for group in utils.iterate_groups():
            document = format_data(
                await get_data_one_group(group, loaders, min_date),
            )
            utils.json_dump(
                document=document,
                entity="group",
                subject=group + utils.get_subject_days(days),
                csv_document=format_csv_data(
                    document=document, header=header, alternative=alternative
                ),
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            document = format_data(
                await get_data_many_groups(
                    org_groups,
                    loaders,
                    min_date,
                ),
            )
            utils.json_dump(
                document=document,
                entity="organization",
                subject=org_id + utils.get_subject_days(days),
                csv_document=format_csv_data(
                    document=document, header=header, alternative=alternative
                ),
            )

        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, groups in await utils.get_portfolios_groups(
                org_name
            ):
                document = format_data(
                    await get_data_many_groups(
                        tuple(groups),
                        loaders,
                        min_date,
                    ),
                )
                utils.json_dump(
                    document=document,
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}"
                    + utils.get_subject_days(days),
                    csv_document=format_csv_data(
                        document=document,
                        header=header,
                        alternative=alternative,
                    ),
                )


def format_data_non_cvssf(data: Remediate) -> dict:
    translations: dict[str, str] = {
        "critical_severity": "Critical",
        "high_severity": "High",
        "medium_severity": "Medium",
        "low_severity": "Low",
    }
    values: list[Decimal] = [
        Decimal(getattr(data, key)).to_integral_exact(rounding=ROUND_CEILING)
        for key, _ in translations.items()
    ]
    max_value: Decimal = list(
        sorted(
            [abs(value) for value in values],
            reverse=True,
        )
    )[0]
    max_axis_value: Decimal = (
        get_max_axis(value=max_value)
        if max_value > Decimal("0.0")
        else Decimal("0.0")
    )

    return dict(
        data=dict(
            columns=[["Mean time to remediate", *values]],
            colors={
                "Mean time to remediate": RISK.neutral,
            },
            labels=True,
            type="bar",
        ),
        bar=dict(
            width=dict(
                ratio=BAR_RATIO_WIDTH,
            ),
        ),
        legend=dict(
            show=False,
        ),
        tooltip=dict(
            show=False,
        ),
        hideXTickLine=True,
        hideYAxisLine=True,
        axis=dict(
            x=dict(
                categories=[value for _, value in translations.items()],
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                    top=0,
                ),
                label=dict(
                    text="Days",
                    position="inner-top",
                ),
                **(
                    {}
                    if max_axis_value == Decimal("0.0")
                    else dict(max=max_axis_value)
                ),
                tick=dict(
                    count=5,
                ),
            ),
        ),
        barChartYTickFormat=True,
        grid=dict(
            y=dict(
                show=True,
            ),
        ),
        mttrCvssf=True,
    )
