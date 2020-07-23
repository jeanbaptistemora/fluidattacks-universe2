# Third party libraries
import pytest

# Local libraries
from forces.utils.aio import unblock


@pytest.mark.asyncio
async def test_unblock():
    result = unblock(print())
    assert str(type(result)) == "<class 'coroutine'>"
