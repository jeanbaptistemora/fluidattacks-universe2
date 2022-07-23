from api.utils.types import (
    ApiDeprecation,
)
from datetime import (
    date,
)
from operator import (
    attrgetter,
)
from typing import (
    Optional,
)


def sort_and_filter_deprecations(
    deprecations: list[ApiDeprecation], end: date, start: Optional[date]
) -> list[ApiDeprecation]:
    """Filters deprecations between the start and end dates (inclusive)"""
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
