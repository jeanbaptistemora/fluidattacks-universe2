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
    Query,
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


def _get_ids_query(proj: ProjectId) -> Query[FrozenList[WidgetId]]:
    return _queries.WidgetIdQuery(
        Transform(lambda t: _from_raw.to_id(*t)),
        proj,
    ).query


def _get_query(widget: WidgetId) -> Query[Widget]:
    return _queries.WidgetQuery(
        Transform(_from_raw.to_obj),
        widget,
    ).query


@dataclass(frozen=True)
class WidgetFactory:
    _client: ApiClient

    def get_ids(self, proj: ProjectId) -> IO[FrozenList[WidgetId]]:
        query = _get_ids_query(proj)
        return self._client.get(query)

    def get(self, widget: WidgetId) -> IO[Widget]:
        query = _get_query(widget)
        return self._client.get(query)
