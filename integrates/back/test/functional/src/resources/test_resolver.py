from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("resources")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_resources(populate: bool, email: str) -> None:
    assert populate
    files: list[dict[str, str]] = [
        {
            "description": "Test",
            "fileName": "test.zip",
            "uploader": "unittest@fluidattacks.com",
            "uploadDate": "2019-03-01 15:21:00",
        },
        {
            "description": "Test",
            "fileName": "shell.exe",
            "uploader": "unittest@fluidattacks.com",
            "uploadDate": "2019-04-24 14:56:00",
        },
        {
            "description": "Test",
            "fileName": "shell2.exe",
            "uploader": "unittest@fluidattacks.com",
            "uploadDate": "2019-04-24 14:59:00",
        },
        {
            "description": "Test",
            "fileName": "asdasd.py",
            "uploader": "unittest@fluidattacks.com",
            "uploadDate": "2019-08-06 14:28:00",
        },
    ]
    result: dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" not in result
    assert "resources" in result["data"]
    assert result["data"]["resources"]["groupName"] == "group1"
    assert result["data"]["resources"]["files"] == files
