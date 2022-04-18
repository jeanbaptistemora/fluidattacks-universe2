from importlib.metadata import (
    version,
)
from jobs_scheduler import (
    __version__,
)
import toml


def test_version() -> None:
    metadata = toml.load("./pyproject.toml")  # type: ignore[misc]
    current: str = metadata["tool"]["poetry"]["version"]  # type: ignore[misc]
    assert __version__ == current
    assert version("jobs_scheduler") == current
