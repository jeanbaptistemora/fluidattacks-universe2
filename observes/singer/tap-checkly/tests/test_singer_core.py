from tap_checkly.singer.core import (
    SingerStreams,
)


def test_unique() -> None:
    assert iter(SingerStreams)
