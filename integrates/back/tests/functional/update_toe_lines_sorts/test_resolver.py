from . import (
    get_result,
    query_get,
)
from .constants import (
    USERS_EMAILS,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.mark.parametrize(["email"], USERS_EMAILS)
async def test_update_toe_lines_sorts(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_nickname="asm_1",
        filename="test2/test.sh",
        sorts_risk_level=10,
    )
    assert result["data"]["updateToeLinesSorts"]["success"]
    result = await query_get(user=email, group_name="group1")
    assert result["data"]["group"]["roots"] == [
        {
            "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "servicesToeLines": [
                {
                    "filename": "test/test#.config",
                    "modifiedDate": "2019-08-01T05:00:00+00:00",
                    "modifiedCommit": "983466z",
                    "loc": 8,
                    "testedDate": "2021-02-28T05:00:00+00:00",
                    "testedLines": 4,
                    "comments": "comment test",
                    "sortsRiskLevel": 0,
                }
            ],
        },
        {
            "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            "servicesToeLines": [
                {
                    "filename": "test2/test.sh",
                    "modifiedDate": "2020-11-19T05:00:00+00:00",
                    "modifiedCommit": "273412t",
                    "loc": 120,
                    "testedDate": "2021-01-20T05:00:00+00:00",
                    "testedLines": 172,
                    "comments": "comment test",
                    "sortsRiskLevel": 10,
                },
                {
                    "filename": "test3/test.config",
                    "modifiedDate": "2020-11-19T05:00:00+00:00",
                    "modifiedCommit": "g545435i",
                    "loc": 55,
                    "testedDate": "2021-01-20T05:00:00+00:00",
                    "testedLines": 33,
                    "comments": "comment test",
                    "sortsRiskLevel": 0,
                },
            ],
        },
    ]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.mark.parametrize(["email"], USERS_EMAILS)
async def test_update_toe_lines_sorts_no_filename(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_nickname="asm_1",
        filename="non_existing_filename",
        sorts_risk_level=10,
    )
    assert (
        result["errors"][0]["message"]
        == "Exception - Toe lines has not been found"
    )
