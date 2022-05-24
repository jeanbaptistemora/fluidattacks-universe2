from ._core import (
    IssueObj,
)
from ._decode import (
    decode_issue_obj,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    UnfoldedJVal,
)
from fa_purity.frozen import (
    freeze,
    unfreeze,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from tap_gitlab.api2._raw import (
    RawClient,
)
from tap_gitlab.api2._raw.page import (
    Page,
)
from typing import (
    Dict,
    Optional,
)


def _to_unfolded(item: UnfoldedJVal) -> UnfoldedJVal:
    return item


@dataclass(frozen=True)
class IssueFilter:
    updated_after: Maybe[datetime]
    updated_before: Maybe[datetime]

    def to_json(self) -> JsonObj:
        after = self.updated_after.map(
            lambda d: {"updated_after": _to_unfolded(d.isoformat())}
        )
        before = self.updated_before.map(
            lambda d: {"updated_before": _to_unfolded(d.isoformat())}
        )
        return (
            after.bind(lambda a: before.map(lambda b: a | b))
            .map(lambda x: freeze(x))
            .map(lambda x: from_unfolded_dict(x))
            .value_or(freeze({}))
        )


@dataclass(frozen=True)
class IssueClient:
    _client: RawClient

    def project_issues(
        self, project_id: int, page: Page, filter: Optional[IssueFilter]
    ) -> Cmd[FrozenList[IssueObj]]:
        raw_args: Dict[str, JsonValue] = {
            "page": JsonValue(page.page_num),
            "per_page": JsonValue(page.per_page),
        }
        if filter:
            raw_args.update(filter.to_json())
        return self._client.get_list(
            f"/projects/{project_id}/issues", freeze(raw_args)
        ).map(lambda l: tuple(map(decode_issue_obj, l)))
