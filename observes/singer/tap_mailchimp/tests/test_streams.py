# Standard libraries
import tempfile
# Third party libraries
import pytest
# Local libraries
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from tap_mailchimp import (
    streams,
)
from tests import (
    mock_client,
)


@pytest.mark.xfail(reason='in development')
def test_all_audiences() -> None:
    client = mock_client.new_client()
    with tempfile.TemporaryFile(mode='w+') as tmp:
        streams.all_audiences(client, target=tmp)
        tmp.seek(0)
        raw_msgs = tmp.readlines()
        singer_msgs = list(map(factory.deserialize, raw_msgs))
        print(singer_msgs)
        n_schemas = len(
            list(filter(lambda x: isinstance(x, SingerSchema), singer_msgs))
        )
        raw_records = list(
            map(
                lambda x: x.record,
                list(filter(lambda x: x is SingerRecord, singer_msgs))
            )
        )
        assert n_schemas == 1
        assert all(
            map(
                lambda audience: client.get_audience(audience) in raw_records,
                client.list_audiences().data['lists']
            )
        )
