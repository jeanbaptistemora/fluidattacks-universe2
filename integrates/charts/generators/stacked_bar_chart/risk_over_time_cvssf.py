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
)


@alru_cache(maxsize=None, typed=True)
async def get_group_document(
    group: str,
    days: int,
) -> Dict[str, Dict[datetime, float]]:
    data: List[GroupDocumentData] = []
    loaders = get_new_context()
    group_loader = loaders.group

    data_name = "remediated_over_time_cvssf"
    if days == 30:
        data_name = f"{data_name}_30"
    elif days == 90:
        data_name = f"{data_name}_90"

    group_data = await group_loader.load(group)
    group_over_time = [elements[-12:] for elements in group_data[data_name]]

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

    return {
        "date": {datum.date: 0 for datum in data},
        "Closed": {datum.date: datum.closed for datum in data},
        "Accepted": {datum.date: datum.accepted for datum in data},
        "Found": {
            datum.date: datum.closed + datum.accepted + datum.opened
            for datum in data
        },
    }


async def get_many_groups_document(
    groups: Iterable[str],
    days: int,
) -> Dict[str, Dict[datetime, float]]:
    group_documents = await collect(
        [get_group_document(group, days) for group in groups]
    )

    return sum_over_time_many_groups(group_documents, RISK_OVER_TIME)


async def generate_all() -> None:
    y_label: str = "CVSSF"
    list_days: List[int] = [0, 30, 90]
    for days in list_days:
        async for group in utils.iterate_groups():
            utils.json_dump(
                document=format_document(
                    document=await get_group_document(group, days),
                    y_label=y_label,
                    tick_format=False,
                ),
                entity="group",
                subject=group + utils.get_subject_days(days),
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            utils.json_dump(
                document=format_document(
                    document=await get_many_groups_document(org_groups, days),
                    y_label=y_label,
                    tick_format=False,
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
                    document=format_document(
                        document=await get_many_groups_document(groups, days),
                        y_label=y_label,
                        tick_format=False,
                    ),
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}"
                    + utils.get_subject_days(days),
                )


if __name__ == "__main__":
    run(generate_all())
