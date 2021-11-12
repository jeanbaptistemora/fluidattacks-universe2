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
    Feed as RawFeed,
)
from tap_announcekit.objs.feed import (
    Feed,
)
from tap_announcekit.objs.id_objs import (
    FeedId,
    ProjectId,
)
from tap_announcekit.streams._query_utils import (
    select_fields,
)
from typing import (
    cast,
    Tuple,
)


@dataclass(frozen=True)
class FeedIdQuery:
    _to_obj: Transform[Tuple[ProjectId, RawFeed], FrozenList[FeedId]]
    proj: ProjectId

    def _select_fields(self, operation: Operation) -> IO[None]:
        items = operation.feeds(project_id=self.proj.id_str)
        items.id()
        return IO(None)

    def query(self) -> Query[FrozenList[FeedId]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: self._to_obj((self.proj, cast(RawFeed, p.feeds)))
            ),
        )


@dataclass(frozen=True)
class FeedQuery:
    _to_obj: Transform[RawFeed, Feed]
    feed: FeedId

    def _select_fields(self, operation: Operation) -> IO[None]:
        item = operation.feed(
            project_id=self.feed.proj.id_str, feed_id=self.feed.id_str
        )
        select_fields(item, frozenset(Feed.__annotations__))
        return IO(None)

    def query(self) -> Query[Feed]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: self._to_obj(
                    cast(RawFeed, p.feed),
                )
            ),
        )
