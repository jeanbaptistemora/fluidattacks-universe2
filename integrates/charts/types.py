from typing import Dict

from typing_extensions import TypedDict


ForcesReport = TypedDict(  # pylint: disable=invalid-name
    "ForcesReport", {"fontSizeRatio": float, "text": str}
)
RemediationReport = TypedDict(  # pylint: disable=invalid-name
    "RemediationReport",
    {
        "current": Dict[str, int],
        "previous": Dict[str, int],
        "totalGroups": int,
    },
)
