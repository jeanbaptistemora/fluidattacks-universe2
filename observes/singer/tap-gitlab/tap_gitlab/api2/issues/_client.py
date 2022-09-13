# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    Stream,
    UnfoldedJVal,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_empty,
)
from tap_gitlab.api2._raw import (
    RawClient,
)
from tap_gitlab.api2._raw.page import (
    Page,
)
from tap_gitlab.api2.ids import (
    ProjectId,
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
    _filter: Optional[IssueFilter]
    _per_page: int = 100

    def project_issues_page(
        self,
        project: ProjectId,
        page: Page,
    ) -> Cmd[FrozenList[IssueObj]]:
        raw_args: Dict[str, JsonValue] = {
            "page": JsonValue(page.page_num),
            "per_page": JsonValue(page.per_page),
        }
        if self._filter:
            raw_args.update(self._filter.to_json())
        return self._client.get_list(
            "/projects/" + project.str_val + "/issues", freeze(raw_args)
        ).map(lambda l: tuple(map(decode_issue_obj, l)))

    def project_issues(self, project: ProjectId) -> Stream[IssueObj]:
        return (
            infinite_range(1, 1)
            .map(lambda i: Page.new_page(i, self._per_page).unwrap())
            .map(lambda p: self.project_issues_page(project, p))
            .transform(lambda x: from_piter(x))
            .map(
                lambda l: Maybe.from_optional(l if l else None).map(
                    lambda x: from_flist(x)
                )
            )
            .transform(lambda x: chain(until_empty(x)))
        )
