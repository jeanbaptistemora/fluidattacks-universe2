from ._client import (
    IssueClient,
    IssueFilter,
)
from ._core import (
    Issue,
    IssueObj,
    IssueType,
)
from tap_gitlab.api2.ids import (
    IssueId,
)

__all__ = [
    "IssueId",
    "IssueType",
    "Issue",
    "IssueObj",
    "IssueFilter",
    "IssueClient",
]
