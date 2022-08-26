from datetime import (
    datetime,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_singer_io.singer import (
    SingerSchema,
)
from tap_mandrill.api.objs.activity import (
    Activity,
)
from tap_mandrill.singer.activity import (
    ActivitySingerEncoder,
)

mock_activity = Activity(
    datetime(2000, 1, 1, 0, 0, 0),
    "receiver@email.com",
    "sender@email.com",
    "The Subject",
    "OK",
    "tag1, tag2",
    "",
    153,
    32,
    "",
)


def test_schema() -> None:
    assert isinstance(ActivitySingerEncoder.schema(), SingerSchema)


def test_record() -> None:
    jschema = ActivitySingerEncoder.schema().schema
    record = ActivitySingerEncoder.to_singer(mock_activity).record
    assert jschema.validate(record).unwrap() is None
    schema_keys = frozenset(
        Unfolder(jschema.encode()["properties"]).to_json().unwrap().keys()
    )
    record_keys = frozenset(record.keys())
    assert schema_keys == record_keys
