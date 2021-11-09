from purity.v1 import (
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.streams.external_users import (
    _encode,
)
from tap_announcekit.streams.external_users._factory import (
    _queries,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)


def test_schema() -> None:
    encoder = _encode.ExtUserObjEncoders("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_external_user)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


ids_query = _queries.ExtUserIdsQuery(
    Transform(lambda _: DataPage(1, 1, 1, tuple())),
    mock_data.mock_proj_id,
    1,
).query
obj_query = _queries.ExtUserQuery(
    Transform(lambda _: mock_data.mock_external_user.obj),
    mock_data.mock_external_user_id,
).query


def test_query_ids() -> None:
    assert ids_query.operation()


def test_query_obj() -> None:
    assert obj_query.operation()


def test_from_data_ids() -> None:
    raw_data = {"data": mock_raw_data.mock_ext_users_ids}
    assert ApiClient.from_data(ids_query, raw_data)


def test_from_data_obj() -> None:
    raw_data = {"data": mock_raw_data.mock_ext_user}
    assert ApiClient.from_data(obj_query, raw_data)
