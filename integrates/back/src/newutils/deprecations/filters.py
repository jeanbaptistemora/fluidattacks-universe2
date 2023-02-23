from datetime import (
    datetime,
)
from newutils.deprecations.types import (
    ApiDeprecation,
)
from operator import (
    attrgetter,
)


def filter_api_deprecation_list(
    deprecations: list[ApiDeprecation],
    end: datetime,
    start: datetime | None,
) -> list[ApiDeprecation]:
    """Filters API deprecations between the start and end dates (inclusive)"""
    filtered_deprs: list[ApiDeprecation] = []
    if start:
        filtered_deprs = [
            deprecation
            for deprecation in deprecations
            if start <= deprecation.due_date <= end
        ]
    else:
        filtered_deprs = [
            deprecation
            for deprecation in deprecations
            if deprecation.due_date <= end
        ]

    return sorted(filtered_deprs, key=attrgetter("parent", "field"))


def filter_api_deprecation_dict(
    depr_dict: dict[str, list[ApiDeprecation]],
    end: datetime,
    start: datetime | None,
) -> dict[str, list[ApiDeprecation]]:
    """Filters API deprecation dicts between the start and end dates
    (inclusive)"""
    filtered_deprs = {
        parent: filter_api_deprecation_list(api_deprecations, end, start)
        for parent, api_deprecations in sorted(depr_dict.items())
    }
    return {
        parent: filtered_api_deprecations
        for parent, filtered_api_deprecations in filtered_deprs.items()
        if filtered_api_deprecations
    }
