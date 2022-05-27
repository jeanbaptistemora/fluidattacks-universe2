from datetime import (
    datetime,
)
from fa_purity import (
    Maybe,
)
from tap_gitlab.api2.ids import (
    EpicId,
    MilestoneId,
    UserId,
)
from tap_gitlab.api2.issues import (
    Issue,
    IssueId,
    IssueType,
)

mock_issue_all_empty = (
    IssueId(123, 55),
    Issue(
        "the title",
        "open",
        IssueType.issue,
        False,
        Maybe.empty(),
        UserId(991),
        0,
        0,
        2,
        (UserId(991), UserId(154)),
        ("label1", "label2"),
        Maybe.empty(),
        Maybe.empty(),
        Maybe.empty(),
        Maybe.empty(),
        Maybe.empty(),
        datetime(2000, 2, 14),
        Maybe.empty(),
        Maybe.empty(),
        Maybe.empty(),
        Maybe.empty(),
    ),
)

mock_issue_full = (
    IssueId(124, 55),
    Issue(
        "the title",
        "closed",
        IssueType.issue,
        False,
        Maybe.from_value(False),
        UserId(533),
        0,
        0,
        2,
        (UserId(533), UserId(4985)),
        ("label1", "label2"),
        Maybe.from_value("description"),
        Maybe.from_value(MilestoneId(11, 45)),
        Maybe.from_value(datetime(2000, 2, 15)),
        Maybe.from_value(EpicId(34, 22)),
        Maybe.from_value(99),
        datetime(2000, 2, 14),
        Maybe.from_value(datetime(2000, 2, 15)),
        Maybe.from_value(datetime(2000, 2, 16)),
        Maybe.from_value(UserId(532)),
        Maybe.from_value("ok"),
    ),
)
