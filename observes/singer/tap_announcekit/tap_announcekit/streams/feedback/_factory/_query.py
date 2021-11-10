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
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.objs.post import (
    Feedback,
)
from tap_announcekit.objs.post.feedback import (
    FeedbackObj,
)
from tap_announcekit.streams.feedback._factory import (
    _from_raw,
)
from typing import (
    Any,
    cast,
    Union,
)

_FeedbackId = Union[ProjectId, PostId]


def _attr_map(attr: str) -> str:
    mapping = {"comment": "feedback"}
    return mapping.get(attr, attr)


def _select_page_fields(fb_page: Any) -> IO[None]:
    props = DataPage.__annotations__.copy()
    del props["items"]
    for attr in props:
        getattr(fb_page, attr)()
    return IO(None)


def _select_item_fields(items: Any) -> IO[None]:
    for attr in Feedback.__annotations__:
        getattr(items, _attr_map(attr))()
    return IO(None)


def _fb_page(id_obj: _FeedbackId, page: int, operation: Operation) -> Any:
    if isinstance(id_obj, PostId):
        return operation.feedbacks(
            project_id=id_obj.proj.id_str, post_id=id_obj.id_str, page=page
        )
    return operation.feedbacks(project_id=id_obj.id_str, page=page)


def _select_fields(
    id_obj: _FeedbackId, page: int, operation: Operation
) -> IO[None]:
    fb_page = _fb_page(id_obj, page, operation)
    items = fb_page.items()
    _select_page_fields(fb_page)
    _select_item_fields(items)
    items.id()
    if isinstance(id_obj, ProjectId):
        items.post_id()
    return IO(None)


@dataclass(frozen=True)
class FeedbackPageQuery:
    page: int

    def query(self, id_obj: _FeedbackId) -> Query[DataPage[FeedbackObj]]:
        return QueryFactory.select(
            partial(_select_fields, id_obj, self.page),
            Transform(
                lambda p: _from_raw.to_page(
                    Transform(partial(_from_raw.to_obj, id_obj)),
                    cast(RawFeedbackPage, p.feedbacks),
                )
            ),
        )
