from charts import (
    utils,
)
from charts.colors import (
    RISK,
)
from charts.generators.bar_chart.utils import (
    Remediate,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)


async def generate_all(
    *,
    format_data: Callable[[Remediate], Dict[str, Any]],
    get_data_one_group: Callable[
        [str, Dataloaders, Optional[date]], Awaitable[Remediate]
    ],
    get_data_many_groups: Callable[
        [Tuple[str, ...], Dataloaders, Optional[date]], Awaitable[Remediate]
    ],
) -> None:
    loaders: Dataloaders = get_new_context()
    list_days: List[int] = [30, 90]
    dates: List[date] = [
        datetime_utils.get_now_minus_delta(days=list_days[0]).date(),
        datetime_utils.get_now_minus_delta(days=list_days[1]).date(),
    ]
    for days, min_date in zip([None, *list_days], [None, *dates]):
        async for group in utils.iterate_groups():
            utils.json_dump(
                document=format_data(
                    await get_data_one_group(group, loaders, min_date),
                ),
                entity="group",
                subject=group + utils.get_subject_days(days),
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            utils.json_dump(
                document=format_data(
                    await get_data_many_groups(
                        org_groups,
                        loaders,
                        min_date,
                    ),
                ),
                entity="organization",
                subject=org_id + utils.get_subject_days(days),
            )

        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, groups in await utils.get_portfolios_groups(
                org_name
            ):
                utils.json_dump(
                    document=format_data(
                        await get_data_many_groups(
                            tuple(groups),
                            loaders,
                            min_date,
                        ),
                    ),
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}"
                    + utils.get_subject_days(days),
                )


def format_data_non_cvssf(data: Remediate) -> dict:
    translations: Dict[str, str] = {
        "critical_severity": "Critical Severity",
        "high_severity": "High Severity",
        "medium_severity": "Medium Severity",
        "low_severity": "Low Severity",
    }
    return dict(
        data=dict(
            columns=[
                ["Mean time to remediate"]
                + [getattr(data, column) for column in translations]
            ],
            colors={
                "Mean time to remediate": RISK.neutral,
            },
            type="bar",
        ),
        axis=dict(
            x=dict(
                categories=[value for _, value in translations.items()],
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                label=dict(
                    text="Calendar days per severity (less is better)",
                    position="inner-top",
                ),
            ),
        ),
        barChartYTickFormat=True,
    )
