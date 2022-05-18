from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
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
    result: Dict[str, Any] = await get_result(
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
