from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_files")
@pytest.mark.parametrize(
    ["user_email", "file_name"],
    [
        ["admin@gmail.com", "test-anim.gif"],
        ["user@gmail.com", "test-file.txt"],
    ],
)
async def test_add_files(
    populate: bool,
    user_email: str,
    file_name: str,
) -> None:
    assert populate
    group_name: str = "group1"

    result: dict[str, Any] = await get_result(
        file_name=file_name,
        group_name=group_name,
        user_email=user_email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["signPostUrl"]
    assert result["data"]["signPostUrl"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_files")
@pytest.mark.parametrize(
    ["user_email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_files_fail(
    populate: bool,
    user_email: str,
) -> None:
    assert populate
    group_name: str = "group1"
    file_name: str = "test-anim.gif"
    result: dict[str, Any] = await get_result(
        file_name=file_name,
        group_name=group_name,
        user_email=user_email,
    )

    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
