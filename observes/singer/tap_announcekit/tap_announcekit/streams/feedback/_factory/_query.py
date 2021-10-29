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
    PostId,
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
    Any,
    cast,
)


def _attr_map(attr: str) -> str:
    mapping = {"comment": "feedback"}
    return mapping.get(attr, attr)


def _select_page_fields(fb_page: Any) -> IO[None]:
    props = FeedbackPage.__annotations__.copy()
    del props["items"]
    for attr in props:
        getattr(fb_page, attr)()
    return IO(None)


def _select_item_fields(items: Any) -> IO[None]:
    for attr in Feedback.__annotations__:
        getattr(items, _attr_map(attr))()
    return IO(None)


def _select_fields(proj: ProjectId, page: int, query: Operation) -> IO[None]:
    fb_page = query.feedbacks(project_id=proj.id_str, page=page)
    items = fb_page.items()
    _select_page_fields(fb_page)
    _select_item_fields(items)
    items.id()
    items.post_id()
    return IO(None)


def _select_fields_2(post: PostId, page: int, query: Operation) -> IO[None]:
    fb_page = query.feedbacks(
        project_id=post.proj.id_str, post_id=post.id_str, page=page
    )
    items = fb_page.items()
    _select_page_fields(fb_page)
    _select_item_fields(items)
    items.id()
    return IO(None)


@dataclass(frozen=True)
class FeedbackPageQuery:
    page: int

    def query(self, proj: ProjectId) -> Query[FeedbackPage]:
        return QueryFactory.select(
            partial(_select_fields, proj, self.page),
            Transform(
                lambda p: _from_raw.to_page(
                    Transform(partial(_from_raw.to_obj, proj)),
                    cast(RawFeedbackPage, p.feedbacks),
                )
            ),
        )

    def query_2(self, post: PostId) -> Query[FeedbackPage]:
        return QueryFactory.select(
            partial(_select_fields_2, post, self.page),
            Transform(
                lambda p: _from_raw.to_page(
                    Transform(partial(_from_raw.to_obj_2, post)),
                    cast(RawFeedbackPage, p.feedbacks),
                )
            ),
        )
