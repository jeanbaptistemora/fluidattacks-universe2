from db_migration import (
    __version__,
)
from importlib.metadata import (
    version,
)
import toml


def test_version() -> None:
    metadata = toml.load("./pyproject.toml")  # type: ignore[misc]
    current: str = metadata["tool"]["poetry"]["version"]  # type: ignore[misc]
    assert __version__ == current
    assert version("db_migration") == current
