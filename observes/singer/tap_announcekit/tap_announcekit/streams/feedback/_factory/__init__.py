from dataclasses import (
    dataclass,
)
from purity.v1 import (
    Transform,
)
from returns.curry import (
    partial,
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
    PageOfFeedback as RawFeedbackPage,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.objs.post import (
    Feedback,
    FeedbackPage,
)
from tap_announcekit.streams.feedback._factory import (
    _from_raw,
)
from typing import (
    cast,
)


@dataclass(frozen=True)
class FeedbackPageQuery:
    proj_id: ProjectId
    page: int

    @staticmethod
    def _attr_map(attr: str) -> str:
        mapping = {"comment": "feedback"}
        return mapping.get(attr, attr)

    def _select_fields(self, query: Operation) -> IO[None]:
        fb_page = query.feedbacks(
            project_id=self.proj_id.id_str, page=self.page
        )
        items = fb_page.items()
        items.id()
        items.post_id()
        for attr in Feedback.__annotations__:
            getattr(items, self._attr_map(attr))()
        props = FeedbackPage.__annotations__.copy()
        del props["items"]
        for attr in props:
            getattr(fb_page, attr)()
        return IO(None)

    def query(self) -> Query[FeedbackPage]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: _from_raw.to_page(
                    Transform(partial(_from_raw.to_obj, self.proj_id)),
                    cast(RawFeedbackPage, p.feedbacks),
                )
            ),
        )
