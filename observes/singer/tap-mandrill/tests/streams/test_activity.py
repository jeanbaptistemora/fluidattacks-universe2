from fa_singer_io.json_schema.core import (
    JsonSchema,
)
from tap_mandrill.streams.activity._encode import (
    ActivitySingerEncoder,
)


def test_schema() -> None:
    assert isinstance(ActivitySingerEncoder.schema(), JsonSchema)
