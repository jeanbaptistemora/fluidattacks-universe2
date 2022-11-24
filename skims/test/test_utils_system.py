import pytest
from utils.system import (
    read,
    read_blocking,
)


@pytest.mark.skims_test_group("unittesting")
def test_read_blocking() -> None:
    code, stdout, stderr = read_blocking("echo", "test")

    assert code == 0
    assert stdout == b"test\n", stdout
    assert not stderr, stderr


@pytest.mark.asyncio
@pytest.mark.skims_test_group("unittesting")
async def test_read() -> None:
    code, stdout, stderr = await read("echo", "test")

    assert code == 0
    assert stdout == b"test\n", stdout
    assert not stderr, stderr
