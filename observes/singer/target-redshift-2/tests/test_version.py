from target_redshift import (
    __version__,
)
import toml


def test_version() -> None:
    metadata = toml.load("./pyproject.toml")  # type: ignore[misc]
    current: str = metadata["tool"]["poetry"]["version"]  # type: ignore[misc]
    assert __version__ == current
