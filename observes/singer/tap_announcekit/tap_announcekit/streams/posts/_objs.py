# pylint: skip-file
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from purity.v1 import (
    FrozenList,
    InvalidType,
    PrimitiveFactory,
)
from returns.maybe import (
    Maybe,
)
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
    Posts as RawPosts,
)
from tap_announcekit.streams.id_objs import (
    ImageId,
    PostId,
    ProjectId,
    UserId,
)
from typing import (
    Any,
    List,
    Optional,
)

JsonStr = str
to_primitive = PrimitiveFactory.to_primitive
to_opt_primitive = PrimitiveFactory.to_opt_primitive


@dataclass(frozen=True)
class _Post:
    # pylint: disable=too-many-instance-attributes
    obj_id: PostId
    user_id: Optional[UserId]
    created_at: datetime
    visible_at: datetime
    image_id: Optional[ImageId]
    expire_at: Optional[datetime]
    updated_at: datetime
    is_draft: bool
    is_pushed: bool
    is_pinned: bool
    is_internal: bool
    external_url: Optional[str]
    segment_filters: Optional[JsonStr]


@dataclass(frozen=True)
class Post(_Post):
    def __init__(self, obj: _Post) -> None:
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)


def _to_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        return raw
    raise InvalidType(f"{type(raw)} expected datetime")


def _to_opt_dt(raw: Any) -> Optional[datetime]:
    return _to_datetime(raw) if raw else None


def _to_maybe_str(raw: Any) -> Maybe[str]:
    return Maybe.from_optional(to_opt_primitive(raw, str) if raw else None)


@dataclass(frozen=True)
class PostFactory:
    @staticmethod
    def to_post(raw: RawPost) -> Post:
        draft = _Post(
            PostId.from_any(raw.project_id, raw.id),
            _to_maybe_str(raw.user_id).map(UserId).value_or(None),
            _to_datetime(raw.created_at),
            _to_datetime(raw.visible_at),
            _to_maybe_str(raw.image_id).map(ImageId).value_or(None),
            _to_opt_dt(raw.expire_at),
            _to_datetime(raw.updated_at),
            to_primitive(raw.is_draft, bool),
            to_primitive(raw.is_pushed, bool),
            to_primitive(raw.is_pinned, bool),
            to_primitive(raw.is_internal, bool),
            to_opt_primitive(raw.external_url, str),
            to_opt_primitive(raw.segment_filters, str),
        )
        return Post(draft)


@dataclass(frozen=True)
class _PostIdPage:
    data: FrozenList[PostId]
    count: int
    page: int
    pages: int


@dataclass(frozen=True)
class PostIdPage(_PostIdPage):
    def __init__(self, obj: _PostIdPage) -> None:
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)


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
