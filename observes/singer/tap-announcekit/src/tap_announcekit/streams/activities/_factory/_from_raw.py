from purity.v1 import (
    PrimitiveFactory,
    Transform,
)
from returns.curry import (
    partial,
)
from tap_announcekit.api.gql_schema import (
    Activity as RawActivity,
    PageOfActivities as RawActivitiesPage,
)
from tap_announcekit.objs.activity import (
    Activity,
    ActivityObj,
)
from tap_announcekit.objs.id_objs import (
    ActivityId,
    ExtUserId,
    FeedbackId,
    IndexedObj,
    PostId,
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.utils import (
    CastUtils,
)

_to_primitive = PrimitiveFactory.to_primitive


def to_obj(proj: ProjectId, raw: RawActivity) -> ActivityObj:
    _id = ActivityId(proj, _to_primitive(raw.id, str))
    post = CastUtils.to_maybe_str(raw.post_id).map(lambda x: PostId(proj, x))
    act = Activity(
        _to_primitive(raw.type, str),
        CastUtils.to_datetime(raw.created_at),
        CastUtils.to_maybe_str(raw.external_user_id)
        .map(lambda x: ExtUserId(proj, x))
        .value_or(None),
        post.value_or(None),
        post.bind(
            lambda p: CastUtils.to_maybe_str(raw.feedback_id).map(
                lambda x: FeedbackId(p, x)
            )
        ).value_or(None),
    )
    return IndexedObj(_id, act)


def to_page(proj: ProjectId, raw: RawActivitiesPage) -> DataPage[ActivityObj]:
    return DataPage(
        _to_primitive(raw.page, int),
        _to_primitive(raw.pages, int),
        _to_primitive(raw.count, int),
        CastUtils.to_flist(raw.items, Transform(partial(to_obj, proj))),
    )
