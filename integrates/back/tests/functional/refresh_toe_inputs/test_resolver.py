from . import (
    query_get,
    refresh_toe_inputs,
)
from _pytest.monkeypatch import (
    MonkeyPatch,
)
from freezegun import (  # type: ignore
    freeze_time,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("refresh_toe_inputs")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-11-10T20:35:20.372236+00:00")
async def test_refresh_toe_inputs(
    populate: bool, email: str, monkeypatch: MonkeyPatch
) -> None:
    assert populate
    group_name = "group1"
    await refresh_toe_inputs(
        user=email,
        group_name=group_name,
        monkeypatch=monkeypatch,
    )
    result = await query_get(user=email, group_name=group_name)
    assert result["data"]["group"]["toeInputs"] == {
        "edges": [
            {
                "node": {
                    "attackedAt": "2020-01-02T05:00:00+00:00",
                    "attackedBy": "",
                    "bePresent": False,
                    "bePresentUntil": "2021-11-10T20:35:20.372236+00:00",
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
            {
                "node": {
                    "attackedAt": "2021-02-11T05:00:00+00:00",
                    "attackedBy": "",
                    "bePresent": True,
                    "bePresentUntil": None,
                    "component": "test.com/test3/test.aspx",
                    "entryPoint": "-",
                    "firstAttackAt": "2021-02-11T05:00:00+00:00",
                    "seenAt": "2020-01-11T05:00:00+00:00",
                    "seenFirstTimeBy": "test3@test.com",
                    "unreliableRootNickname": "test_nickname_3",
                },
                "cursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI0NPTVBPTkVOVCN0ZXN0LmNvbS90ZXN0My90ZXN0LmFzcHgjRU5UUllQT0lOVCMtIn0=",
            },
        ],
        "pageInfo": {
            "hasNextPage": False,
            "endCursor": "eyJwayI6ICJHUk9VUCNncm91cDEiLCAic2siOiAiSU5QVVRTI0NPTVBPTkVOVCN0ZXN0LmNvbS90ZXN0My90ZXN0LmFzcHgjRU5UUllQT0lOVCMtIn0=",
        },
    }
