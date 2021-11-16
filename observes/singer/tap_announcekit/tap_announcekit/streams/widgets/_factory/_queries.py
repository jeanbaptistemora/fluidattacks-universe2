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
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    Widget as RawWidget,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
    WidgetId,
)
from tap_announcekit.objs.widget import (
    Widget,
)
from tap_announcekit.streams._query_utils import (
    select_fields,
)
from typing import (
    cast,
    List,
    Tuple,
)


@dataclass(frozen=True)
class WidgetIdQuery:
    _to_obj: Transform[Tuple[ProjectId, RawWidget], WidgetId]
    proj: ProjectId

    def _select_fields(self, operation: Operation) -> IO[None]:
        items = operation.widgets(project_id=self.proj.id_str)
        items.id()
        return IO(None)

    @property
    def query(self) -> Query[FrozenList[WidgetId]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: tuple(
                    self._to_obj((self.proj, f))
                    for f in cast(List[RawWidget], p.widgets)
                )
            ),
        )


@dataclass(frozen=True)
class WidgetQuery:
    _to_obj: Transform[RawWidget, Widget]
    widget: WidgetId

    def _select_fields(self, operation: Operation) -> IO[None]:
        item = operation.widget(
            project_id=self.widget.proj.id_str, widget_id=self.widget.id_str
        )
        select_fields(item, frozenset(Widget.__annotations__))
        return IO(None)

    @property
    def query(self) -> Query[Widget]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: self._to_obj(
                    cast(RawWidget, p.widget),
                )
            ),
        )
