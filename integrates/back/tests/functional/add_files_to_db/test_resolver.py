from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_files_to_db")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_add_files_to_db(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    file_name: str = "test-anim.gif"
    description: str = "test description"
    first_modifier_email: str = "admin@gmail.com"

    result: dict[str, Any] = await get_result(
        description=description,
        file_name=file_name,
        group_name=group_name,
        user_email=email,
    )
    assert "errors" not in result
    assert result["data"]["addFilesToDb"]["success"]

    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group_typed.load(group_name)
    assert group.files
    file_uploaded = next(
        file for file in group.files if file.file_name == file_name
    )
    assert file_uploaded.description == description
    assert file_uploaded.file_name == file_name
    assert file_uploaded.modified_by == first_modifier_email
    assert file_uploaded.modified_date is not None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_files_to_db")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_files_to_db_fail(populate: bool, email: str) -> None:
    assert populate
    description: str = "test description"
    filename: str = "test-anim.gif"
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        description=description,
        file_name=filename,
        group_name=group_name,
        user_email=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
