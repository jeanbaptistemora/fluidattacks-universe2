from purity.v1 import (
    PrimitiveFactory,
    Transform,
)
from tap_announcekit.api.gql_schema import (
    Feedback as RawFeedback,
    PageOfFeedback as RawFeedbackPage,
)
from tap_announcekit.objs.id_objs import (
    ExtUserId,
    FeedbackId,
    IndexedObj,
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post import (
    Feedback,
    FeedbackObj,
    FeedbackPage,
)
from tap_announcekit.objs.post.feedback import (
    ActionSource,
)
from tap_announcekit.utils import (
    CastUtils,
)
from typing import (
    Union,
)

_to_primitive = PrimitiveFactory.to_primitive
_to_opt_primitive = PrimitiveFactory.to_opt_primitive
_FeedbackId = Union[ProjectId, PostId]


def to_feedback(proj: ProjectId, raw: RawFeedback) -> Feedback:
    return Feedback(
        _to_opt_primitive(raw.reaction, str),
        _to_opt_primitive(raw.feedback, str),
        ActionSource(raw.source),
        CastUtils.to_datetime(raw.created_at),
        ExtUserId(proj, _to_primitive(raw.external_user_id, str)),
    )


def to_obj(id_obj: _FeedbackId, raw: RawFeedback) -> FeedbackObj:
    proj = id_obj if isinstance(id_obj, ProjectId) else id_obj.proj
    feedback = to_feedback(proj, raw)
    post_id = (
        PostId(id_obj, _to_primitive(raw.post_id, str))
        if isinstance(id_obj, ProjectId)
        else id_obj
    )
    _id = FeedbackId(
        post_id,
        _to_primitive(raw.id, str),
    )
    return IndexedObj(_id, feedback)


def to_page(
    to_fb_obj: Transform[RawFeedback, FeedbackObj], raw: RawFeedbackPage
) -> FeedbackPage:
    return FeedbackPage(
        _to_primitive(raw.page, int),
        _to_primitive(raw.pages, int),
        _to_primitive(raw.count, int),
        CastUtils.to_flist(
            raw.items,
            to_fb_obj,
        ),
    )
