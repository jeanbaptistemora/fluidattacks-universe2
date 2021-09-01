from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
        ["hacker@fluidattacks.com"],
        ["closer@fluidattacks.com"],
        ["customer@fluidattacks.com"],
        ["customeradmin@fluidattacks.com"],
        ["executive@fluidattacks.com"],
        ["group_manager@fluidattacks.com"],
        ["resourcer@fluidattacks.com"],
        ["reviewer@fluidattacks.com"],
    ],
)
async def test_get_toe_lines(populate: bool, email: str) -> None:
    assert populate
    comments: str = "comment test"
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["data"]["group"]["roots"] == [
        {
            "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "toeLines": [
                {
                    "filename": "product/test/test#.config",
                    "modifiedDate": "2019-08-01T00:00:00-05:00",
                    "modifiedCommit": "983466z",
                    "loc": 8,
                    "testedDate": "2021-02-28T00:00:00-05:00",
                    "testedLines": 4,
                    "comments": comments,
                }
            ],
        },
        {
            "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            "toeLines": [
                {
                    "filename": "asm_1/test2/test.sh",
                    "modifiedDate": "2020-11-19T00:00:00-05:00",
                    "modifiedCommit": "273412t",
                    "loc": 172,
                    "testedDate": "2021-01-20T00:00:00-05:00",
                    "testedLines": 120,
                    "comments": comments,
                },
                {
                    "filename": "asm_1/test3/test.config",
                    "modifiedDate": "2020-11-19T00:00:00-05:00",
                    "modifiedCommit": "g545435i",
                    "loc": 55,
                    "testedDate": "2021-01-20T00:00:00-05:00",
                    "testedLines": 33,
                    "comments": comments,
                },
            ],
        },
    ]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["group_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["service_forces@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_error(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["errors"][0]["message"] == "Access denied"
