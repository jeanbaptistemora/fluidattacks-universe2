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
from tap_announcekit.objs.id_objs import (
    ProjectId,
    WidgetId,
)
from tap_announcekit.objs.widget import (
    Widget,
)
from tap_announcekit.streams.widgets._factory import (
    _from_raw,
    _queries,
)


@dataclass(frozen=True)
class WidgetFactory:
    _client: ApiClient

    def get_ids(self, proj: ProjectId) -> IO[FrozenList[WidgetId]]:
        query = _queries.WidgetIdQuery(
            Transform(lambda t: _from_raw.to_id(t[0], t[1])),
            proj,
        ).query
        return self._client.get(query)

    def get(self, feed: WidgetId) -> IO[Widget]:
        query = _queries.WidgetQuery(
            Transform(_from_raw.to_obj),
            feed,
        ).query
        return self._client.get(query)
