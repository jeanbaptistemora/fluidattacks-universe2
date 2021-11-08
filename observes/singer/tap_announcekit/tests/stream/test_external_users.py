from purity.v1 import (
    Transform,
)
import pytest
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
    utils,
)


def test_schema() -> None:
    encoder = _encode.ExtUserObjEncoders("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_external_user)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


@pytest.mark.xfail(reason="in development")
def test_query_ids() -> None:
    query = _queries.ExtUserIdsQuery(
        Transform(lambda _: DataPage(1, 1, 1, tuple())),
        mock_data.mock_proj_id,
        1,
    ).query
    assert query.operation()


@pytest.mark.xfail(reason="in development")
def test_query_obj() -> None:
    query = _queries.ExtUserQuery(
        Transform(lambda _: mock_data.mock_external_user.obj),
        mock_data.mock_external_user_id,
    ).query
    assert query.operation()
