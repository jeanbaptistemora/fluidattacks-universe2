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
    pure_map,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
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

    def get_page(self) -> Cmd[FrozenList[CheckStatusObj]]:
        return self._client.get_list(
            "/v1/check-statuses",
            from_prim_dict({}),
        ).map(
            lambda l: pure_map(
                lambda i: CheckStatusDecoder(i).decode_obj().unwrap(), l
            ).to_list()
        )

    def list_all(self) -> Stream[CheckStatusObj]:
        return (
            from_piter(from_flist((self.get_page(),)))
            .map(lambda x: from_flist(x))
            .transform(lambda x: chain(x))
        )

    @staticmethod
    def new(
        auth: Credentials,
        per_page: int,
    ) -> CheckStatusClient:
        return CheckStatusClient(RawClient(auth), per_page)
