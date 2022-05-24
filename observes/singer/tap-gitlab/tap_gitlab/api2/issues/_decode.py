from ._core import (
    Issue,
    IssueType,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    JsonObj,
    JsonValue,
    Maybe,
)
from fa_purity.json.value.transform import (
    Unfolder,
    UnfoldResult,
)
from tap_gitlab.api2.ids import (
    EpicId,
    MilestoneId,
    UserId,
)


def _extract_user(item: JsonValue) -> UnfoldResult[UserId]:
    return (
        Unfolder(item)
        .to_unfolder_dict()
        .bind(lambda x: x["id"].to_primitive(str))
        .map(UserId)
    )


def _extract_user_or_fail(item: JsonValue) -> UserId:
    return _extract_user(item).unwrap()


@dataclass(frozen=True)
class _Ids:
    id: str
    iid: int


def _extract_ids(item: Unfolder) -> UnfoldResult[_Ids]:
    return item.to_unfolder_dict().map(
        lambda x: _Ids(
            x["id"].to_primitive(str).unwrap(),
            x["iid"].to_primitive(int).unwrap(),
        )
    )


def _extract_milestone(item: Unfolder) -> UnfoldResult[MilestoneId]:
    return _extract_ids(item).map(lambda i: MilestoneId(i.id, i.iid))


def _extract_epic(item: Unfolder) -> UnfoldResult[EpicId]:
    return _extract_ids(item).map(lambda i: EpicId(i.id, i.iid))


def decode_issue(raw: JsonObj) -> Issue:
    return Issue(
        Unfolder(raw["title"]).to_primitive(str).unwrap(),
        Unfolder(raw["state"]).to_primitive(str).unwrap(),
        Unfolder(raw["issue_type"])
        .to_primitive(str)
        .map(lambda x: IssueType(x))
        .unwrap(),
        Unfolder(raw["confidential"]).to_primitive(bool).unwrap(),
        Unfolder(raw["discussion_locked"]).to_primitive(bool).unwrap(),
        _extract_user(raw["author"]).unwrap(),
        Unfolder(raw["upvotes"]).to_primitive(int).unwrap(),
        Unfolder(raw["downvotes"]).to_primitive(int).unwrap(),
        Unfolder(raw["merge_requests_count"]).to_primitive(int).unwrap(),
        Unfolder(raw["assignees"])
        .to_list()
        .map(lambda l: tuple(map(_extract_user_or_fail, l)))
        .unwrap(),
        Unfolder(raw["labels"]).to_list_of(str).unwrap(),
        Unfolder(raw["description"])
        .to_optional(lambda u: u.to_primitive(str))
        .map(lambda x: Maybe.from_optional(x))
        .unwrap(),
        Unfolder(raw["milestone"])
        .to_optional(_extract_milestone)
        .map(lambda x: Maybe.from_optional(x))
        .unwrap(),
        Unfolder(raw["due_date"])
        .to_optional(lambda u: u.to_primitive(str))
        .map(
            lambda x: Maybe.from_optional(x).map(
                lambda d: datetime.strptime(d, "%Y-%m-%d").date()
            )
        )
        .unwrap(),
        Maybe.from_optional(raw.get("epic")).bind_optional(
            lambda j: Unfolder(j).to_optional(_extract_epic).unwrap()
        ),
        Maybe.from_optional(raw.get("weight")).bind_optional(
            lambda j: Unfolder(j)
            .to_optional(lambda x: x.to_primitive(int))
            .unwrap()
        ),
        Unfolder(raw["created_at"]).to_primitive(str).map(isoparse).unwrap(),
        Unfolder(raw["updated_at"])
        .to_optional(lambda s: s.to_primitive(str).map(isoparse))
        .map(lambda x: Maybe.from_optional(x))
        .unwrap(),
        Unfolder(raw["closed_at"])
        .to_optional(lambda s: s.to_primitive(str).map(isoparse))
        .map(lambda x: Maybe.from_optional(x))
        .unwrap(),
        Unfolder(raw["closed_by"])
        .to_optional(lambda s: _extract_user(s.jval))
        .map(lambda x: Maybe.from_optional(x))
        .unwrap(),
        Maybe.from_optional(raw.get("health_status")).bind_optional(
            lambda j: Unfolder(j)
            .to_optional(lambda x: x.to_primitive(str))
            .unwrap()
        ),
    )
