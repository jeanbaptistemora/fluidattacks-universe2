# Third party libraries
import pytest

# Local libraries
from apis.asserts import (
    create_exploit_blocking,
    execute,
)


def test_create_exploit_blocking():
    with create_exploit_blocking('content') as file:
        assert file.read().decode() == 'content'


@pytest.mark.asyncio
async def test_execute():
    process = await execute('')

    assert process.returncode == 0
    assert b'vulnerabilities: 0' in await process.stdout.read()
