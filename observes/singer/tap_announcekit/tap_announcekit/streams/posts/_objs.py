# pylint: skip-file
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from returns.maybe import (
    Maybe,
)
from singer_io.singer2.json import (
    InvalidType,
    to_opt_primitive,
    to_primitive,
)
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
)
from tap_announcekit.streams.id_objs import (
    ImageId,
    PostId,
    UserId,
)
from typing import (
    Any,
    Optional,
)

JsonStr = str


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


@dataclass(frozen=True)
class PostFactory(_Post):
    @classmethod
    def _to_datetime(cls, raw: Any) -> datetime:
        if isinstance(raw, datetime):
            return raw
        raise InvalidType(f"{type(raw)} expected datetime")

    @classmethod
    def _to_opt_dt(cls, raw: Any) -> Optional[datetime]:
        return cls._to_datetime(raw) if raw else None

    @classmethod
    def _to_maybe_str(cls, raw: Any) -> Maybe[str]:
        return Maybe.from_optional(to_opt_primitive(raw, str) if raw else None)

    @classmethod
    def to_post(cls, raw: RawPost) -> Post:
        draft = _Post(
            PostId.from_any(raw.project_id, raw.id),
            cls._to_maybe_str(raw.user_id).map(UserId).value_or(None),
            cls._to_datetime(raw.created_at),
            cls._to_datetime(raw.visible_at),
            cls._to_maybe_str(raw.image_id).map(ImageId).value_or(None),
            cls._to_opt_dt(raw.expire_at),
            cls._to_datetime(raw.updated_at),
            to_primitive(raw.is_draft, bool),
            to_primitive(raw.is_pushed, bool),
            to_primitive(raw.is_pinned, bool),
            to_primitive(raw.is_internal, bool),
            to_opt_primitive(raw.external_url, str),
            to_opt_primitive(raw.segment_filters, str),
        )
        return Post(draft)


__all__ = ["PostId"]
