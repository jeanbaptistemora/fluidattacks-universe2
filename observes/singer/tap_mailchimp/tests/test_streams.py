# Standard libraries
import tempfile
from typing import Union

# Third party libraries

# Local libraries
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from tap_mailchimp import (
    api,
    streams,
)
from tests import (
    mock_client,
)


AudienceId = Union[api.AudienceId]


def test_all_audiences() -> None:
    # Arrange
    client = mock_client.new_client()
    with tempfile.TemporaryFile(mode='w+') as tmp:
        # Act
        streams.all_audiences(client, target=tmp)
        tmp.seek(0)
        raw_msgs = tmp.readlines()
        singer_msgs = list(map(factory.deserialize, raw_msgs))
        n_schemas = len(
            list(filter(lambda x: isinstance(x, SingerSchema), singer_msgs))
        )
        raw_records = list(map(
            lambda x: x.record,
            list(filter(lambda x: isinstance(x, SingerRecord), singer_msgs))
        ))
        audiences = list(map(
            lambda x: AudienceId(x['id']),
            client.list_audiences().data['lists']
        ))
        # Assert
        assert n_schemas == 0
        for audience in audiences:
            assert client.get_audience(audience).data in raw_records
