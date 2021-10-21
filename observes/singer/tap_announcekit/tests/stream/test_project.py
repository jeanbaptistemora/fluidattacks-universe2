from tap_announcekit.streams.project._encode import (
    ProjectEncoders,
)
from tap_announcekit.streams.project._getters import (
    ProjectQuery,
)


def test_query() -> None:
    ProjectQuery("1234").query().operation()


def test_schema() -> None:
    assert ProjectEncoders.encoder("stream_1").schema
