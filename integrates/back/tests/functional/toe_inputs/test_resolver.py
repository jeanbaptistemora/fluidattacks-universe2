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
        ["customer_manager@fluidattacks.com"],
        ["hacker@fluidattacks.com"],
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
                    "root": {
                        "__typename": "GitRoot",
                        "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
                        "nickname": "test_nickname_1",
                    },
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI1J"
                "PT1QjNjMyOThhNzMtOWRmZi00NmNmLWI0MmQtOWIyZjAxYTU2Nj"
                "kwI0NPTVBPTkVOVCN0ZXN0LmNvbS9hcGkvVGVzdCNFTlRSWVBPS"
                "U5UI2lkVGVzdCJ9",
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
                    "root": {
                        "__typename": "GitRoot",
                        "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                        "nickname": "test_nickname_2",
                    },
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI1J"
                "PT1QjNzY1YjFkMGYtYjZmYi00NDg1LWI0ZTItMmMyY2IxNTU1Yj"
                "FhI0NPTVBPTkVOVCN0ZXN0LmNvbS90ZXN0Mi90ZXN0LmFzcHgjR"
                "U5UUllQT0lOVCMtIn0=",
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
                    "root": None,
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI1J"
                "PT1QjQ09NUE9ORU5UI3Rlc3QuY29tL3Rlc3QvdGVzdC5hc3B4I0"
                "VOVFJZUE9JTlQjYnRuVGVzdCJ9",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI1JP"
            "T1QjQ09NUE9ORU5UI3Rlc3QuY29tL3Rlc3QvdGVzdC5hc3B4I0VO"
            "VFJZUE9JTlQjYnRuVGVzdCJ9",
        },
    }


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_inputs")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["architect@fluidattacks.com"],
        ["architect@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@fluidattacks.com"],
        ["reattacker@gmail.com"],
        ["user@fluidattacks.com"],
        ["user@gmail.com"],
        ["user_manager@fluidattacks.com"],
        ["user_manager@gmail.com"],
        ["executive@fluidattacks.com"],
        ["executive@gmail.com"],
        ["customer_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@fluidattacks.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_get_toe_inputs_error(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["errors"][0]["message"] == "Access denied"
