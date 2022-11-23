from purity.v1 import (
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.streams.labels import (
    _encode,
)
from tap_announcekit.streams.labels._factory import (
    LabelFactory,
    LabelsQuery,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)


def test_schema() -> None:
    encoder = _encode.LabelObjEncoders("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_label_obj)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


def test_build_query_obj() -> None:
    assert LabelsQuery(
        Transform(lambda _: mock_data.mock_label_obj.obj),
        mock_data.mock_proj_id,
    ).query.operation()


def test_query_obj() -> None:
    # pylint: disable=protected-access
    # test should be able to call protected members
    raw_data = {"data": mock_raw_data.mock_labels}
    assert ApiClient.from_data(
        LabelFactory._get_query(mock_data.mock_proj_id), raw_data
    )
