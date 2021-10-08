from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    TREATMENT,
)
from charts.generators.pie_chart.utils import (
    generate_all,
)
from groups import (
    domain as groups_domain,
)
from typing import (
    Dict,
    NamedTuple,
    Tuple,
)

Treatment = NamedTuple(
    "Treatment",
    [
        ("acceptedUndefined", int),
        ("accepted", int),
        ("inProgress", int),
        ("undefined", int),
    ],
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Treatment:
    item = await groups_domain.get_attributes(group, ["total_treatment"])

    treatment = item.get("total_treatment", {})

    return Treatment(
        acceptedUndefined=treatment.get("acceptedUndefined", 0),
        accepted=treatment.get("accepted", 0),
        inProgress=treatment.get("inProgress", 0),
        undefined=treatment.get("undefined", 0),
    )


async def get_data_many_groups(groups: Tuple[str, ...]) -> Treatment:
    groups_data = await collect(map(get_data_one_group, list(groups)))

    return Treatment(
        acceptedUndefined=sum(
            [group.acceptedUndefined for group in groups_data]
        ),
        accepted=sum([group.accepted for group in groups_data]),
        inProgress=sum([group.inProgress for group in groups_data]),
        undefined=sum([group.undefined for group in groups_data]),
    )


def format_data(data: Treatment) -> dict:
    translations: Dict[str, str] = {
        "acceptedUndefined": "Permanently accepted",
        "accepted": "Temporarily Accepted",
        "inProgress": "In Progress",
        "undefined": "Not defined",
    }

    return {
        "data": {
            "columns": [
                [value, str(getattr(data, key))]
                for key, value in translations.items()
            ],
            "type": "pie",
            "colors": {
                "Permanently accepted": TREATMENT.more_passive,
                "Temporarily Accepted": TREATMENT.passive,
                "In Progress": TREATMENT.neutral,
                "Not defined": TREATMENT.more_agressive,
            },
        },
        "legend": {
            "position": "right",
        },
        "pie": {
            "label": {
                "show": True,
            },
        },
    }


if __name__ == "__main__":
    run(
        generate_all(
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            format_document=format_data,
        )
    )
