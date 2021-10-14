# pylint: skip-file
from dataclasses import (
    dataclass,
)
from purity.v1 import (
    InvalidType,
    PrimitiveFactory,
)
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
    Posts as RawPosts,
)
from tap_announcekit.objs.id_objs import (
    ImageId,
    PostId,
    ProjectId,
    UserId,
)
from tap_announcekit.objs.post import (
    _Post,
    Post,
)
from tap_announcekit.objs.post_page import (
    _PostIdPage,
    PostIdPage,
)
from tap_announcekit.utils import (
    CastUtils,
)
from typing import (
    Any,
    List,
)

JsonStr = str
to_primitive = PrimitiveFactory.to_primitive
to_opt_primitive = PrimitiveFactory.to_opt_primitive


@dataclass(frozen=True)
class PostFactory:
    @staticmethod
    def to_post(raw: RawPost) -> Post:
        draft = _Post(
            PostId.from_any(raw.project_id, raw.id),
            CastUtils.to_maybe_str(raw.user_id).map(UserId).value_or(None),
            CastUtils.to_datetime(raw.created_at),
            CastUtils.to_datetime(raw.visible_at),
            CastUtils.to_maybe_str(raw.image_id).map(ImageId).value_or(None),
            CastUtils.to_opt_dt(raw.expire_at),
            CastUtils.to_datetime(raw.updated_at),
            to_primitive(raw.is_draft, bool),
            to_primitive(raw.is_pushed, bool),
            to_primitive(raw.is_pinned, bool),
            to_primitive(raw.is_internal, bool),
            to_opt_primitive(raw.external_url, str),
            to_opt_primitive(raw.segment_filters, str),
        )
        return Post(draft)


def _to_list(raw: Any) -> List[Any]:
    if isinstance(raw, list):
        return raw
    raise InvalidType(f"{type(raw)} expected List[Any]")


@dataclass(frozen=True)
class PostPageFactory(_Post):
    @staticmethod
    def to_post_page(raw: RawPosts) -> PostIdPage:
        draft = _PostIdPage(
            tuple(
                PostId.from_any(i.project_id, i.id) for i in _to_list(raw.list)
            ),
            to_primitive(raw.count, int),
            to_primitive(raw.page, int),
            to_primitive(raw.pages, int),
        )
        return PostIdPage(draft)


__all__ = [
    "PostId",
    "ProjectId",
]
