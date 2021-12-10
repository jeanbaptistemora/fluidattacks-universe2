from . import (
    get_result,
    query_get,
)
from freezegun import (  # type: ignore
    freeze_time,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-11-10T20:35:20.372236+00:00")
async def test_update_toe_lines_attacked_lines_set_lines(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
        filenames=["test/test#.config", "test2/test.sh", "test3/test.config"],
        attacked_at="2021-05-05T07:00:00+00:00",
        attacked_lines=8,
        comments="edited comments 1",
    )
    assert result["data"]["updateToeLinesAttackedLines"]["success"]
    result = await query_get(user=email, group_name="group1")
    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2021-05-05T07:00:00+00:00",
                    "attackedBy": "admin@fluidattacks.com",
                    "attackedLines": 8,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "edited comments 1",
                    "commitAuthor": "customer1@gmail.com",
                    "filename": "test/test#.config",
                    "firstAttackAt": "2021-05-05T07:00:00+00:00",
                    "loc": 4324,
                    "modifiedCommit": "273412t",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "product",
                    },
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdC90ZXN0Iy5jb25maWcifQ==",
            },
            {
                "node": {
                    "attackedAt": "2021-05-05T07:00:00+00:00",
                    "attackedBy": "admin@fluidattacks.com",
                    "attackedLines": 8,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "edited comments 1",
                    "commitAuthor": "customer2@gmail.com",
                    "filename": "test2/test.sh",
                    "firstAttackAt": "2020-02-19T15:41:04+00:00",
                    "loc": 8,
                    "modifiedCommit": "983466z",
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "root": {
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "product",
                    },
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdDIvdGVzdC5zaCJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-05-05T07:00:00+00:00",
                    "attackedBy": "admin@fluidattacks.com",
                    "attackedLines": 8,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "edited comments 1",
                    "commitAuthor": "customer3@gmail.com",
                    "filename": "test3/test.config",
                    "firstAttackAt": "2020-01-14T15:41:04+00:00",
                    "loc": 243,
                    "modifiedCommit": "g545435i",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "product",
                    },
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 80,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdDMvdGVzdC5jb25maWcifQ==",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdDMvdGVzdC5jb25maWcifQ==",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-11-10T20:35:20.372236+00:00")
async def test_update_toe_lines_attacked_lines_not_set_lines(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
        filenames=["test/test#.config", "test2/test.sh", "test3/test.config"],
        attacked_at="2021-05-06T07:00:00+00:00",
        attacked_lines=None,
        comments="edited comments 2",
    )
    assert result["data"]["updateToeLinesAttackedLines"]["success"]
    result = await query_get(user=email, group_name="group1")
    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2021-05-06T07:00:00+00:00",
                    "attackedBy": "admin@fluidattacks.com",
                    "attackedLines": 4324,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "edited comments 2",
                    "commitAuthor": "customer1@gmail.com",
                    "filename": "test/test#.config",
                    "firstAttackAt": "2021-05-05T07:00:00+00:00",
                    "loc": 4324,
                    "modifiedCommit": "273412t",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "product",
                    },
                    "seenAt": "2020-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 0,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdC90ZXN0Iy5jb25maWcifQ==",
            },
            {
                "node": {
                    "attackedAt": "2021-05-06T07:00:00+00:00",
                    "attackedBy": "admin@fluidattacks.com",
                    "attackedLines": 8,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "edited comments 2",
                    "commitAuthor": "customer2@gmail.com",
                    "filename": "test2/test.sh",
                    "firstAttackAt": "2020-02-19T15:41:04+00:00",
                    "loc": 8,
                    "modifiedCommit": "983466z",
                    "modifiedDate": "2020-11-15T15:41:04+00:00",
                    "root": {
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "product",
                    },
                    "seenAt": "2020-02-01T15:41:04+00:00",
                    "sortsRiskLevel": -1,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdDIvdGVzdC5zaCJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-05-06T07:00:00+00:00",
                    "attackedBy": "admin@fluidattacks.com",
                    "attackedLines": 243,
                    "bePresent": True,
                    "bePresentUntil": "",
                    "comments": "edited comments 2",
                    "commitAuthor": "customer3@gmail.com",
                    "filename": "test3/test.config",
                    "firstAttackAt": "2020-01-14T15:41:04+00:00",
                    "loc": 243,
                    "modifiedCommit": "g545435i",
                    "modifiedDate": "2020-11-16T15:41:04+00:00",
                    "root": {
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "product",
                    },
                    "seenAt": "2019-01-01T15:41:04+00:00",
                    "sortsRiskLevel": 80,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdDMvdGVzdC5jb25maWcifQ==",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiTElORVMjUk9PVCM2MzI5OGE3My05ZGZmLTQ2Y2YtYjQyZC05YjJmMDFhNTY2OTAjRklMRU5BTUUjdGVzdDMvdGVzdC5jb25maWcifQ==",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["architect@fluidattacks.com"],
        ["hacker@fluidattacks.com"],
        ["reattacker@fluidattacks.com"],
        ["customer@fluidattacks.com"],
        ["customeradmin@fluidattacks.com"],
        ["executive@fluidattacks.com"],
        ["system_owner@fluidattacks.com"],
        ["resourcer@fluidattacks.com"],
        ["reviewer@fluidattacks.com"],
        ["service_forces@fluidattacks.com"],
        ["architect@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["system_owner@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_update_toe_lines_attacked_lines_access_denied(
    populate: bool, email: str
) -> None:
    assert populate
    assert populate
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
        filenames=["test/test#.config", "test2/test.sh", "test3/test.config"],
        attacked_at="2021-05-05T07:00:00+00:00",
        attacked_lines=8,
        comments="edited comments 1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_update_toe_lines_attacked_lines_invalid_attacked_at(
    populate: bool, email: str
) -> None:
    assert populate
    assert populate
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
        filenames=["test/test#.config", "test2/test.sh", "test3/test.config"],
        attacked_at="2021-05-05T07:00:00+00:00",
        attacked_lines=8,
        comments="edited comments 1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == (
        "Exception - The attack time must be between the previous attack "
        "and the current time"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_update_toe_lines_attacked_lines_invalid_attacked_lines(
    populate: bool, email: str
) -> None:
    assert populate
    assert populate
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
        filenames=["test/test#.config", "test2/test.sh", "test3/test.config"],
        attacked_at="2021-05-06T07:00:00+00:00",
        attacked_lines=5000,
        comments="edited comments 1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == (
        "Exception - The attack time must be between the previous attack "
        "and the current time"
    )
