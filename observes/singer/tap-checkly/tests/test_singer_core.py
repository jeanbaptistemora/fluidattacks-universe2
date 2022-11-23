from tap_checkly.singer import (
    SingerStreams,
)


def test_unique() -> None:
    assert iter(SingerStreams)
