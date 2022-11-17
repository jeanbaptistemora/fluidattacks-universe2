# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.skip(reason="The mutation has not been developed")
@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8080",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8081",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e6",
        ],
    ],
)
async def test_add_toe_port(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addToePort"]
    assert result["data"]["addToePort"]["success"]
