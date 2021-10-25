from datetime import (
    datetime,
)
from tap_announcekit.objs.id_objs import (
    ExtUserId,
    FeedbackId,
    IndexedObj,
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post.feedback import (
    ActionSource,
    Feedback,
    FeedbackObj,
)
from tap_announcekit.streams.feedback import (
    _encode,
)

mock_proj_id = ProjectId("proj1234")
mock_feedback_obj: FeedbackObj = IndexedObj(
    FeedbackId(PostId(mock_proj_id, "post346"), "feedback99"),
    Feedback(
        ":)",
        "comment",
        ActionSource.EMAIL,
        datetime(2000, 1, 1),
        ExtUserId(mock_proj_id, "extUser100"),
    ),
)


def test_schema() -> None:
    encoder = _encode.FeedbackObjEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_feedback_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
