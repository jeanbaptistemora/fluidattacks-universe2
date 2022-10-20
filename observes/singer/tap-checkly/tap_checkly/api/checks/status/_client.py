# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from ._decode import (
    CheckStatusDecoder,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Stream,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
    pure_map,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_none,
)
from tap_checkly.api._raw import (
    Credentials,
    RawClient,
)
from tap_checkly.objs import (
    CheckStatusObj,
)


@dataclass(frozen=True)
class CheckStatusClient:
    _client: RawClient
    _per_page: int

    def _get_page(self, page: int) -> Cmd[FrozenList[CheckStatusObj]]:
        return self._client.get_list(
            "/v1/check-statuses",
            from_prim_dict(
                {
                    "limit": self._per_page,
                    "page": page,
                }
            ),
        ).map(
            lambda l: pure_map(
                lambda i: CheckStatusDecoder(i).decode_obj().unwrap(), l
            ).to_list()
        )

    def list_all(self) -> Stream[CheckStatusObj]:
        return (
            infinite_range(1, 1)
            .map(self._get_page)
            .transform(lambda x: from_piter(x))
            .map(lambda i: i if bool(i) else None)
            .transform(lambda x: until_none(x))
            .map(lambda x: from_flist(x))
            .transform(lambda x: chain(x))
        )

    @staticmethod
    def new(
        auth: Credentials,
        per_page: int,
    ) -> CheckStatusClient:
        return CheckStatusClient(RawClient(auth), per_page)
