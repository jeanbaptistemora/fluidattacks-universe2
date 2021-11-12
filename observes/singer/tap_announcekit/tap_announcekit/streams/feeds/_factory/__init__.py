from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
    Transform,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.feed import (
    Feed,
)
from tap_announcekit.objs.id_objs import (
    FeedId,
    ProjectId,
)
from tap_announcekit.streams.feeds._factory import (
    _from_raw,
    _queries,
)


@dataclass(frozen=True)
class FeedFactory:
    _client: ApiClient

    def get_ids(self, proj: ProjectId) -> IO[FrozenList[FeedId]]:
        query = _queries.FeedIdQuery(
            Transform(lambda t: _from_raw.to_id(t[0], t[1])),
            proj,
        ).query
        return self._client.get(query)

    def get(self, feed: FeedId) -> IO[Feed]:
        query = _queries.FeedQuery(
            Transform(_from_raw.to_obj),
            feed,
        ).query
        return self._client.get(query)
