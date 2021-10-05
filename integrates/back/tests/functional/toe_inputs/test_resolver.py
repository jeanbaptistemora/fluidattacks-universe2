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
    assert result["data"]["group"]["toeInputs"] == [
        {
            "commit": "hh66uu5",
            "component": "test.com/api/Test",
            "createdDate": "2000-01-01T00:00:00-05:00",
            "entryPoint": "idTest",
            "seenFirstTimeBy": "",
            "testedDate": "2020-01-02T00:00:00-05:00",
            "unreliableRootNickname": "test_nickname_1",
            "verified": "Yes",
            "vulns": "FIN.S.0001.Test",
        },
        {
            "commit": "e91320h",
            "component": "test.com/test/test.aspx",
            "createdDate": "2020-03-14T00:00:00-05:00",
            "entryPoint": "btnTest",
            "seenFirstTimeBy": "test@test.com",
            "testedDate": "2021-02-02T00:00:00-05:00",
            "unreliableRootNickname": "",
            "verified": "No",
            "vulns": "",
        },
        {
            "commit": "d83027t",
            "component": "test.com/test2/test.aspx",
            "createdDate": "2020-01-11T00:00:00-05:00",
            "entryPoint": "-",
            "seenFirstTimeBy": "test2@test.com",
            "testedDate": "2021-02-11T00:00:00-05:00",
            "unreliableRootNickname": "test_nickname_2",
            "verified": "No",
            "vulns": "FIN.S.0003.Test",
        },
    ]


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
