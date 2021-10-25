from tap_announcekit.streams.project._encode import (
    ProjectEncoders,
)
from tap_announcekit.streams.project._getters import (
    ProjectQuery,
)
from tests.stream import (
    mock_data,
)


def test_query() -> None:
    ProjectQuery("1234").query().operation()


# @pytest.mark.xfail(reason="future fix")
def test_schema() -> None:
    encoder = ProjectEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_proj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())
