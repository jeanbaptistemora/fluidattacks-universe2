from purity.v1 import (
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.streams.widgets import (
    _encode,
)
from tap_announcekit.streams.widgets._factory import (
    _get_ids_query,
    _get_query,
    _queries,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)


def test_schema() -> None:
    encoder = _encode.WidgetObjEncoders("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_widget_obj)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


def test_build_query_id() -> None:
    assert _queries.WidgetIdQuery(
        Transform(lambda _: mock_data.mock_widget_obj.id_obj),
        mock_data.mock_proj_id,
    ).query.operation()


def test_build_query_obj() -> None:
    assert _queries.WidgetQuery(
        Transform(lambda _: mock_data.mock_widget_obj.obj),
        mock_data.mock_widget_obj.id_obj,
    ).query.operation()


def test_query_id() -> None:
    raw_data = {"data": mock_raw_data.mock_widgets_ids}
    assert ApiClient.from_data(
        _get_ids_query(mock_data.mock_proj_id), raw_data
    )


def test_query_obj() -> None:
    raw_data = {"data": mock_raw_data.mock_widget}
    assert ApiClient.from_data(
        _get_query(mock_data.mock_widget_obj.id_obj), raw_data
    )
