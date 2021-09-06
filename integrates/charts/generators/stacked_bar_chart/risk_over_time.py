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
from charts.generators.stacked_bar_chart.utils import (
    format_document,
    GroupDocumentData,
    RISK_OVER_TIME,
    sum_over_time_many_groups,
    translate_date,
    translate_date_last,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from typing import (
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
)


class RiskOverTime(NamedTuple):
    monthly: Dict[str, Dict[datetime, float]]
    weekly: Dict[str, Dict[datetime, float]]
    should_use_monthly: bool


@alru_cache(maxsize=None, typed=True)
async def get_group_document(  # pylint: disable=too-many-locals
    group: str, days: Optional[int] = None
) -> RiskOverTime:
    data: List[GroupDocumentData] = []
    data_monthly: List[GroupDocumentData] = []
    context = get_new_context()
    group_loader = context.group

    data_name_monthly = "remediated_over_time_month"
    data_name = "remediated_over_time"
    if days == 30:
        data_name = f"{data_name}_30"
    elif days == 90:
        data_name = f"{data_name}_90"

    group_data = await group_loader.load(group)
    group_over_time = [
        # Last 12 weeks
        elements[-12:]
        for elements in group_data[data_name]
    ]
    group_over_time_monthly = [
        elements[-12:] for elements in group_data[data_name_monthly]
    ]

    if group_over_time:
        group_found_over_time = group_over_time[0]
        group_closed_over_time = group_over_time[1]
        group_accepted_over_time = group_over_time[2]

        for accepted, closed, found in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_found_over_time,
        ):
            data.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=found["y"] - closed["y"] - accepted["y"],
                    date=translate_date(found["x"]),
                    total=found["y"],
                )
            )
    else:
        print(f"[WARNING] {group} has no remediated_over_time attribute")

    if group_over_time_monthly:
        group_found_over_time = group_over_time_monthly[0]
        group_closed_over_time = group_over_time_monthly[1]
        group_accepted_over_time = group_over_time_monthly[2]

        for accepted, closed, found in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_found_over_time,
        ):
            data_monthly.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=found["y"] - closed["y"] - accepted["y"],
                    date=(
                        translate_date_last(found["x"])
                        if translate_date_last(found["x"]) < datetime.now()
                        else datetime.combine(
                            datetime.now(),
                            datetime.min.time(),
                        )
                    ),
                    total=found["y"],
                )
            )

    return RiskOverTime(
        should_use_monthly=False
        if days
        else len(group_data[data_name][0] if group_data[data_name] else [])
        > 12,
        monthly={
            "date": {datum.date: 0 for datum in data_monthly},
            "Closed": {datum.date: datum.closed for datum in data_monthly},
            "Accepted": {datum.date: datum.accepted for datum in data_monthly},
            "Found": {
                datum.date: datum.closed + datum.accepted + datum.opened
                for datum in data_monthly
            },
        },
        weekly={
            "date": {datum.date: 0 for datum in data},
            "Closed": {datum.date: datum.closed for datum in data},
            "Accepted": {datum.date: datum.accepted for datum in data},
            "Found": {
                datum.date: datum.closed + datum.accepted + datum.opened
                for datum in data
            },
        },
    )


async def get_many_groups_document(
    groups: Iterable[str], days: Optional[int] = None
) -> Dict[str, Dict[datetime, float]]:
    group_documents: Tuple[RiskOverTime, ...] = await collect(
        [get_group_document(group, days) for group in groups]
    )
    should_use_monthly: bool = any(
        [group.should_use_monthly for group in group_documents]
    )

    return sum_over_time_many_groups(
        [group_document.monthly for group_document in group_documents]
        if should_use_monthly
        else [group_document.weekly for group_document in group_documents],
        RISK_OVER_TIME,
    )


async def generate_all() -> None:
    y_label: str = "Vulnerabilities"
    async for group in utils.iterate_groups():
        group_document: RiskOverTime = await get_group_document(group)
        utils.json_dump(
            document=format_document(
                document=group_document.monthly
                if group_document.should_use_monthly
                else group_document.weekly,
                y_label=y_label,
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_document(
                document=await get_many_groups_document(org_groups),
                y_label=y_label,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_document(
                    document=await get_many_groups_document(groups),
                    y_label=y_label,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )

    # Limit days
    list_days: List[int] = [30, 90]
    for days in list_days:
        async for group in utils.iterate_groups():
            utils.json_dump(
                document=format_document(
                    document=(await get_group_document(group, days)).weekly,
                    y_label=y_label,
                ),
                entity="group",
                subject=f"{group}_{days}",
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            utils.json_dump(
                document=format_document(
                    document=await get_many_groups_document(org_groups, days),
                    y_label=y_label,
                ),
                entity="organization",
                subject=f"{org_id}_{days}",
            )

        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, groups in await utils.get_portfolios_groups(
                org_name
            ):
                utils.json_dump(
                    document=format_document(
                        document=await get_many_groups_document(groups, days),
                        y_label=y_label,
                    ),
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}_{days}",
                )


if __name__ == "__main__":
    run(generate_all())
