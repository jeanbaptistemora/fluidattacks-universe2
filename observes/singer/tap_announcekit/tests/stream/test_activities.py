from purity.v1 import (
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.streams.activities import (
    _encode,
)
from tap_announcekit.streams.activities._factory import (
    _queries,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)


def test_schema() -> None:
    encoder = _encode.ActivityObjEncoder("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_act_obj)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


obj_query = _queries.ActivitiesQuery(
    Transform(lambda _: DataPage(0, 1, 1, tuple([mock_data.mock_act_obj]))),
    mock_data.mock_proj_id,
    0,
).query


def test_query_obj() -> None:
    assert obj_query.operation()


def test_from_data_obj() -> None:
    raw_data = {"data": mock_raw_data.mock_activities}
    assert ApiClient.from_data(obj_query, raw_data)
