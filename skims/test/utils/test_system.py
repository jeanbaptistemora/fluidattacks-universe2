# Local libraries
from utils.system import (
    call,
)

# Third party libraries
import pytest


@pytest.mark.asyncio  # type: ignore
async def test_call() -> None:
    process = await call('echo', 'test')

    stdout: bytes = await process.stdout.read() if process.stdout else bytes()

    assert stdout == 'test\n'.encode(), process
