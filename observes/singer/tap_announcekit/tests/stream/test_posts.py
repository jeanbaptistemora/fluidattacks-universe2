from tap_announcekit.streams.posts._encode import (
    PostEncoder,
)


def test_schema() -> None:
    PostEncoder.schema()
