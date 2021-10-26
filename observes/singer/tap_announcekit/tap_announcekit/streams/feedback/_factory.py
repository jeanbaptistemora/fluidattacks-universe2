from purity.v1 import (
    PrimitiveFactory,
    Transform,
)
from returns.curry import (
    partial,
)
from tap_announcekit.api.gql_schema import (
    ActionSource,
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
from tap_announcekit.utils import (
    CastUtils,
)

_to_primitive = PrimitiveFactory.to_primitive
_to_opt_primitive = PrimitiveFactory.to_opt_primitive


def _to_obj(proj: ProjectId, raw: RawFeedback) -> FeedbackObj:
    feedback = Feedback(
        _to_opt_primitive(raw.reaction, str),
        _to_opt_primitive(raw.feedback, str),
        ActionSource(raw.source),
        CastUtils.to_datetime(raw.created_at),
        ExtUserId(proj, _to_primitive(raw.external_user_id, str)),
    )
    _id = FeedbackId(
        PostId(proj, _to_primitive(raw.post_id, str)),
        _to_primitive(raw.id, str),
    )
    return IndexedObj(_id, feedback)


def _to_page(proj: ProjectId, raw: RawFeedbackPage) -> FeedbackPage:
    return FeedbackPage(
        _to_primitive(raw.page, int),
        _to_primitive(raw.pages, int),
        _to_primitive(raw.count, int),
        CastUtils.to_flist(
            raw.items,
            Transform(partial(_to_obj, proj)),
        ),
    )
