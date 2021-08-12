from tap_announcekit.stream.project._builders import (
    proj_query,
)


def test_query() -> None:
    proj_query("1234")
