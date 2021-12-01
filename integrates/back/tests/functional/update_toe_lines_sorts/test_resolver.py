from . import (
    get_result,
    query_get,
    query_services_get,
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
    services_result = await query_services_get(user=email, group_name="group1")
    assert services_result["data"]["group"]["roots"] == [
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
    result = await query_get(user=email, group_name="group1")
    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test@test.com",
                    "attackedLines": 23,
                    "bePresent": False,
                    "bePresentUntil": "2021-01-19T15:41:04+00:00",
                    "comments": "comment 1",
                    "commitAuthor": "customer1@gmail.com",
                    "filename": "test/test#.config",
                    "firstAttackAt": "2020-01-19T15:41:04+00:00",
                    "loc": 4324,
                    "modifiedCommit": "273412t",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {"nickname": "product"},
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdC90ZXN0Iy5jb25maWcifQ==",
            },
            {
                "node": {
                    "attackedAt": "2021-02-20T05:00:00+00:00",
                    "attackedBy": "test2@test.com",
                    "attackedLines": 4,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "comment 2",
                    "commitAuthor": "customer2@gmail.com",
                    "filename": "test2/test.sh",
                    "firstAttackAt": "2020-02-19T15:41:04+00:00",
                    "loc": 8,
                    "modifiedCommit": "983466z",
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "root": {"nickname": "asm_1"},
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": 10,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjRklMRU5BTUUjdGVzdDIvdGVzdC5zaCJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-01-20T05:00:00+00:00",
                    "attackedBy": "test3@test.com",
                    "attackedLines": 120,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "comment 3",
                    "commitAuthor": "customer3@gmail.com",
                    "filename": "test3/test.config",
                    "firstAttackAt": "2020-01-14T15:41:04+00:00",
                    "loc": 243,
                    "modifiedCommit": "g545435i",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {"nickname": "asm_1"},
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjRklMRU5BTUUjdGVzdDMvdGVzdC5jb25maWcifQ==",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM3NjViMWQwZi1iNmZiLTQ0ODUtYjRlMi0yYzJjYjE1NTViMWEjRklMRU5BTUUjdGVzdDMvdGVzdC5jb25maWcifQ==",
        },
    }


@pytest.mark.skip
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
