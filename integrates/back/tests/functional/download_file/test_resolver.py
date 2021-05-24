# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("download_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
    ],
)
async def test_download_file(populate: bool, email: str):
    assert populate
    file_name: str = "test.zip"
    result: Dict[str, Any] = await query(
        user=email,
        group="group1",
        f_name=file_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["downloadFile"]
    assert result["data"]["downloadFile"]["success"]
    assert "url" in result["data"]["downloadFile"]
