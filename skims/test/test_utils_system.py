# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from utils.system import (
    read,
    blocking_read,
)


@pytest.mark.skims_test_group('unittesting')
def blocking_test_read() -> None:
    code, stdout, stderr = blocking_read('echo', 'test')

    assert code == 0
    assert stdout == b'test\n', stdout
    assert not stderr, stderr


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_read() -> None:
    code, stdout, stderr = await read('echo', 'test')

    assert code == 0
    assert stdout == b'test\n', stdout
    assert not stderr, stderr
