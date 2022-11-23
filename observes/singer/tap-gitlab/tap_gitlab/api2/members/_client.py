from ._core import (
    Member,
)
from ._decode import (
    decode_member,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonValue,
    Maybe,
    Stream,
)
from fa_purity.frozen import (
    freeze,
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
)


@dataclass(frozen=True)
class MembersClient:
    _client: RawClient
    _per_page: int = 100

    def _member_page(
        self,
        project: ProjectId,
        page: Page,
    ) -> Cmd[FrozenList[Member]]:
        raw_args: Dict[str, JsonValue] = {
            "page": JsonValue(page.page_num),
            "per_page": JsonValue(page.per_page),
        }
        return self._client.get_list(
            "/projects/" + project.str_val + "/members/all", freeze(raw_args)
        ).map(lambda l: tuple(map(decode_member, l)))

    def project_members(self, project: ProjectId) -> Stream[Member]:
        return (
            infinite_range(1, 1)
            .map(lambda i: Page.new_page(i, self._per_page).unwrap())
            .map(lambda p: self._member_page(project, p))
            .transform(lambda x: from_piter(x))
            .map(
                lambda l: Maybe.from_optional(l if l else None).map(
                    lambda x: from_flist(x)
                )
            )
            .transform(lambda x: chain(until_empty(x)))
        )
