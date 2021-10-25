from tap_announcekit.streams.feedback import (
    _encode,
)
from tests.stream import (
    mock_data,
)


def test_schema() -> None:
    encoder = _encode.FeedbackObjEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_feedback_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())
