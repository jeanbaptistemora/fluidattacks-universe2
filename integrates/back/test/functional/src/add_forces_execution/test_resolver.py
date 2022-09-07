# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.forces.types import (
    ForcesExecution,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_forces_execution")
@pytest.mark.parametrize(
    ["email"],
    [
        ["service_forces@gmail.com"],
    ],
)
async def test_add_forces_execution(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" not in result
    assert result["data"]["addForcesExecution"]["success"]

    group = "group1"
    execution: str = "18c1e735a73243f2ab1ee0757041f80e"
    loaders = get_new_context()
    force_execution: ForcesExecution = await loaders.forces_execution.load(
        (group, execution)
    )
    assert force_execution.id == execution
    assert force_execution.branch == "master"
    assert force_execution.commit == "2e7b34c1358db2ff4123c3c76e7fe3bf9f2838f2"
    assert force_execution.execution_date == "2020-02-20T00:00:00+00:00"
    assert force_execution.vulnerabilities.num_of_accepted_vulnerabilities == 1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_forces_execution")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_forces_execution_fail(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
