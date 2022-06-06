from __future__ import (
    annotations,
)

from . import (
    _decode,
)
from ._core import (
    AlertChannelObj,
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
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_none,
)
from tap_checkly.api2._raw import (
    Credentials,
    RawClient,
)


@dataclass(frozen=True)
class AlertChannelsClient:
    _client: RawClient
    _per_page: int

    def _get_page(self, page: int) -> Cmd[FrozenList[AlertChannelObj]]:
        return self._client.get_list(
            "/v1/alert-channels",
            from_prim_dict(
                {
                    "limit": self._per_page,
                    "page": page,
                }
            ),
        ).map(lambda l: tuple(map(_decode.from_raw_obj, l)))

    def list_all(self) -> Stream[AlertChannelObj]:
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
    ) -> AlertChannelsClient:
        return AlertChannelsClient(RawClient(auth), per_page)
