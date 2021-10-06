from typing import (
    Dict,
)
from typing_extensions import (
    TypedDict,
)

ForcesReport = TypedDict("ForcesReport", {"fontSizeRatio": float, "text": str})
RemediationReport = TypedDict(
    "RemediationReport",
    {
        "current": Dict[str, int],
        "previous": Dict[str, int],
        "totalGroups": int,
    },
)
