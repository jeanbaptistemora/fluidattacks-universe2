from . import (
    get_result,
)
from freezegun import (
    freeze_time,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_lines")
@pytest.mark.parametrize(
    ["email", "filename", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "test/test1.py",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
    ],
)
async def test_add_toe_lines(
    populate: bool,
    email: str,
    filename: str,
    root_id: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        filename=filename,
        group_name="group1",
        root_id=root_id,
        last_author="test@test.com",
        last_commit="d9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4",
        loc=50,
        modified_date="2020-11-19T13:37:10+00:00",
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addToeLines"]
    assert result["data"]["addToeLines"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_lines")
@pytest.mark.parametrize(
    ["email", "filename", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "test/test2.py",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
        [
            "admin@fluidattacks.com",
            "test/test3.py",
            "eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
        ],
    ],
)
async def test_add_toe_lines_fail_git_root(
    populate: bool,
    email: str,
    filename: str,
    root_id: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        filename=filename,
        group_name="group1",
        root_id=root_id,
        last_author="test@test.com",
        last_commit="d9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4",
        loc=50,
        modified_date="2020-11-19T13:37:10+00:00",
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"] == "Exception - A git root is required"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_lines")
@pytest.mark.parametrize(
    ["email", "filename", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "test/test1.py",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
    ],
)
async def test_add_toe_lines_fail_last_author(
    populate: bool,
    email: str,
    filename: str,
    root_id: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        filename=filename,
        group_name="group1",
        root_id=root_id,
        last_author="test_author",
        last_commit="d9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4",
        loc=50,
        modified_date="2020-11-19T13:37:10+00:00",
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Invalid email address in form"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_lines")
@pytest.mark.parametrize(
    ["email", "filename", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "test/test1.py",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
    ],
)
async def test_add_toe_lines_fail_last_commit(
    populate: bool,
    email: str,
    filename: str,
    root_id: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        filename=filename,
        group_name="group1",
        root_id=root_id,
        last_author="test@test.com",
        last_commit="d9e4beba70c4f34d6",
        loc=50,
        modified_date="2020-11-19T13:37:10+00:00",
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The commit hash is invalid"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_lines")
@pytest.mark.parametrize(
    ["email", "filename", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "test/test1.py",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
    ],
)
@freeze_time("2019-03-31")
async def test_add_toe_lines_fail_modified_date(
    populate: bool,
    email: str,
    filename: str,
    root_id: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        filename=filename,
        group_name="group1",
        root_id=root_id,
        last_author="test@test.com",
        last_commit="d9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4",
        loc=50,
        modified_date="2020-11-19T13:37:10+00:00",
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The modified date can not be a future date"
    )
