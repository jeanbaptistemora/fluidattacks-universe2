from tap_announcekit.streams.project._encode import (
    ProjectEncoder,
)
from tap_announcekit.streams.project._getters import (
    _proj_query,
)


def test_query() -> None:
    _proj_query("1234")


def test_schema() -> None:
    ProjectEncoder.schema()
