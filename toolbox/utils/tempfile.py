# Standard library
import contextlib
import tempfile
import textwrap
from typing import (
    Generator,
)


@contextlib.contextmanager
def create(
    suffix: str,
    content: str,
) -> Generator[str, None, None]:
    """Creates a tempfile.NamedTemporaryFile and yields its name."""
    content = content[1:]
    content = textwrap.dedent(content)
    with tempfile.NamedTemporaryFile(suffix=suffix) as file:
        file.write(content.encode())
        file.seek(0)

        yield file.name
