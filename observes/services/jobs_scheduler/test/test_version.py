from importlib.metadata import (
    version,
)
from jobs_scheduler import (
    __version__,
)
import toml


def test_version() -> None:
    metadata = toml.load("./pyproject.toml")
    current: str = metadata["tool"]["poetry"]["version"]
    assert __version__ == current
    assert version("jobs_scheduler") == current
