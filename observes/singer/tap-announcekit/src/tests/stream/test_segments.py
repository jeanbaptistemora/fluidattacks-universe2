from purity.v1 import (
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
)
from tap_announcekit.streams.segments import (
    _encode,
)
from tap_announcekit.streams.segments._factory import (
    _get_segment_profs,
    _get_segments_query,
    _queries,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)


def test_field_schema() -> None:
    encoder = _encode.SegmentFieldEncoder("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_segment_field)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


def test_profile_schema() -> None:
    encoder = _encode.SegmentProfileEncoder("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_segment_prof)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


def test_build_field_query() -> None:
    assert _queries.SegmentFieldQuery(
        Transform(lambda _: "foo"),
        mock_data.mock_proj_id,
    ).query.operation()


def test_build_profile_query() -> None:
    assert _queries.SegmentProfileQuery(
        Transform(lambda _: IndexedObj("foo_id", "foo")),
        mock_data.mock_proj_id,
    ).query.operation()


def test_field_query() -> None:
    raw_data = {"data": mock_raw_data.mock_segments}
    assert ApiClient.from_data(
        _get_segments_query(mock_data.mock_proj_id), raw_data
    )


def test_query_obj() -> None:
    raw_data = {"data": mock_raw_data.mock_segments_prof}
    assert ApiClient.from_data(
        _get_segment_profs(mock_data.mock_proj_id), raw_data
    )
