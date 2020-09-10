# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from utils.system import (
    read,
)


@run_decorator
async def test_read() -> None:
    code, stdout, stderr = await read('echo', 'test')

    assert code == 0
    assert stdout == b'test\n', stdout
    assert not stderr, stderr
