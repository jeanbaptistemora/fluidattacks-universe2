# Third party libraries
from aioextensions import (
    block_decorator,
)

# Local libraries
from utils.system import (
    call,
)


@block_decorator
async def test_call() -> None:
    process = await call('echo', 'test')

    stdout: bytes = await process.stdout.read() if process.stdout else bytes()

    assert stdout == 'test\n'.encode(), process
