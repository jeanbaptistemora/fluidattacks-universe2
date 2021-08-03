from singer_io.singer2 import (
    SingerDeserializer,
    SingerRecord,
    SingerSchema,
)
from tap_mailchimp import (
    api,
    streams,
)
import tempfile
from tests import (
    mock_client,
)
from typing import (
    cast,
    Union,
)

AudienceId = Union[api.AudienceId]


def test_all_audiences() -> None:
    # Arrange
    client = mock_client.new_client()
    with tempfile.TemporaryFile(mode="w+") as tmp:
        # Act
        streams.all_audiences(client, target=tmp)
        tmp.seek(0)
        raw_msgs = tmp.readlines()
        singer_msgs = list(map(SingerDeserializer.deserialize, raw_msgs))
        n_schemas = len(
            list(filter(lambda x: isinstance(x, SingerSchema), singer_msgs))
        )
        raw_records = list(
            map(
                lambda x: cast(SingerRecord, x).record,
                list(
                    filter(lambda x: isinstance(x, SingerRecord), singer_msgs)
                ),
            )
        )
        audiences = client.list_audiences()
        # Assert
        assert n_schemas == 0
        for audience in audiences:
            assert client.get_audience(audience).data in raw_records
