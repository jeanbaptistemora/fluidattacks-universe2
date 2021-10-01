from charts.colors import (
    RISK,
)
from decimal import (
    Decimal,
)
from operator import (
    attrgetter,
)
from typing import (
    cast,
    List,
    NamedTuple,
    Union,
)

PortfoliosGroupsInfo = NamedTuple(
    "PortfoliosGroupsInfo",
    [
        ("group_name", str),
        ("value", Decimal),
    ],
)

MAX_GROUPS_DISPLAYED = 4


def slice_groups(
    groups_data: List[PortfoliosGroupsInfo], total_value: Decimal
) -> List[PortfoliosGroupsInfo]:
    groups_data_sorted = sorted(
        groups_data, key=attrgetter("value"), reverse=True
    )
    groups_data_sliced = groups_data_sorted[:MAX_GROUPS_DISPLAYED]

    if len(groups_data_sorted) > MAX_GROUPS_DISPLAYED:
        return groups_data_sliced + [
            PortfoliosGroupsInfo(
                group_name="others",
                value=total_value
                - sum([group.value for group in groups_data_sliced]),
            )
        ]

    return groups_data_sliced


def format_data(groups_data: List[PortfoliosGroupsInfo]) -> dict:
    return dict(
        data=dict(
            # pylint: disable=unsubscriptable-object
            columns=[
                cast(List[Union[Decimal, str]], [group.group_name])
                + [group.value]
                for group in groups_data
            ],
            type="pie",
            colors=dict(
                (group.group_name, color)
                for group, color in zip(groups_data, reversed(RISK))
            ),
        ),
        legend=dict(
            position="right",
        ),
        pie=dict(
            label=dict(
                show=True,
            ),
        ),
    )
