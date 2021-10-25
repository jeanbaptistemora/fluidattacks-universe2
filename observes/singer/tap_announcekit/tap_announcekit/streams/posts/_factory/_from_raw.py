# pylint: skip-file
from purity.v1 import (
    PrimitiveFactory,
)
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
    Posts as RawPosts,
)
from tap_announcekit.objs.id_objs import (
    ImageId,
    IndexedObj,
    PostId,
    UserId,
)
from tap_announcekit.objs.post import (
    Post,
    PostIdPage,
    PostObj,
)
from tap_announcekit.utils import (
    CastUtils,
)
from typing import (
    cast,
    List,
)

JsonStr = str
to_primitive = PrimitiveFactory.to_primitive
to_opt_primitive = PrimitiveFactory.to_opt_primitive


def to_post(raw: RawPost) -> PostObj:
    post = Post(
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
    return IndexedObj(PostId.from_any(raw.project_id, raw.id), post)


def to_post_page(raw: RawPosts) -> PostIdPage:
    return PostIdPage(
        tuple(
            PostId.from_any(i.project_id, i.id)
            for i in cast(List[RawPost], CastUtils.to_list(raw.list))
        ),
        to_primitive(raw.count, int),
        to_primitive(raw.page, int),
        to_primitive(raw.pages, int),
    )
