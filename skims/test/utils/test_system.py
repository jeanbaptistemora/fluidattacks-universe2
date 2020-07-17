# Local libraries
from utils.system import (
    call,
)

# Third party libraries
import pytest


@pytest.mark.asyncio  # type: ignore
async def test_call() -> None:
    process = await call('echo', 'test')

    assert await process.stdout.read() == 'test\n'.encode(), process
