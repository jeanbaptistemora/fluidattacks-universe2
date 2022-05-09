from batch_stability import (
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
    assert version("batch_stability") == current
