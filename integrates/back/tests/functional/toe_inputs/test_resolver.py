from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_inputs")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
        ["hacker@fluidattacks.com"],
        ["reattacker@fluidattacks.com"],
        ["customer@fluidattacks.com"],
        ["customeradmin@fluidattacks.com"],
        ["executive@fluidattacks.com"],
        ["system_owner@fluidattacks.com"],
        ["resourcer@fluidattacks.com"],
        ["reviewer@fluidattacks.com"],
    ],
)
async def test_get_toe_inputs(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["data"]["group"]["toeInputs"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2020-01-02T05:00:00+00:00",
                    "attackedBy": "",
                    "bePresent": True,
                    "bePresentUntil": None,
                    "component": "test.com/api/Test",
                    "entryPoint": "idTest",
                    "firstAttackAt": "2020-01-02T05:00:00+00:00",
                    "seenAt": "2000-01-01T05:00:00+00:00",
                    "seenFirstTimeBy": "",
                    "unreliableRootNickname": "test_nickname_1",
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI0NPTVBPTkVOVCN0ZXN0LmNvbS9hcGkvVGVzdCNFTlRSWVBPSU5UI2lkVGVzdCJ9",
            },
            {
                "node": {
                    "attackedAt": "2021-02-02T05:00:00+00:00",
                    "attackedBy": "",
                    "bePresent": True,
                    "bePresentUntil": None,
                    "component": "test.com/test/test.aspx",
                    "entryPoint": "btnTest",
                    "firstAttackAt": "2021-02-02T05:00:00+00:00",
                    "seenAt": "2020-03-14T05:00:00+00:00",
                    "seenFirstTimeBy": "test@test.com",
                    "unreliableRootNickname": "",
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI0NPTVBPTkVOVCN0ZXN0LmNvbS90ZXN0L3Rlc3QuYXNweCNFTlRSWVBPSU5UI2J0blRlc3QifQ==",
            },
            {
                "node": {
                    "attackedAt": "2021-02-11T05:00:00+00:00",
                    "attackedBy": "",
                    "bePresent": False,
                    "bePresentUntil": "2021-03-11T05:00:00+00:00",
                    "component": "test.com/test2/test.aspx",
                    "entryPoint": "-",
                    "firstAttackAt": "2021-02-11T05:00:00+00:00",
                    "seenAt": "2020-01-11T05:00:00+00:00",
                    "seenFirstTimeBy": "test2@test.com",
                    "unreliableRootNickname": "test_nickname_2",
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI0NPTVBPTkVOVCN0ZXN0LmNvbS90ZXN0Mi90ZXN0LmFzcHgjRU5UUllQT0lOVCMtIn0=",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI0NPTVBPTkVOVCN0ZXN0LmNvbS90ZXN0Mi90ZXN0LmFzcHgjRU5UUllQT0lOVCMtIn0=",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_inputs")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["system_owner@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["service_forces@fluidattacks.com"],
    ],
)
async def test_get_toe_inputs_error(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["errors"][0]["message"] == "Access denied"
