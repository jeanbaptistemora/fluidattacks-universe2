from tap_announcekit.stream.project import (
    proj_query,
)


def test_query() -> None:
    proj_query("1234")
