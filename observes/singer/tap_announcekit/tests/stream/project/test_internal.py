from tap_announcekit.stream.project._builders import (
    proj_query,
)
from tap_announcekit.stream.project._encode import (
    ProjectEncoder,
)


def test_query() -> None:
    proj_query("1234")


def test_proj_schema() -> None:
    ProjectEncoder.schema()
