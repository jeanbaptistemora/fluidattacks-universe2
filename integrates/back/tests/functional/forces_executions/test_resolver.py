from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("forces_executions")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_get_forces_executions(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    executions = result["data"]["forcesExecutions"]["executions"]
    assert (
        result["data"]["forcesExecutions"]["fromDate"]
        == "2020-02-01 00:00:00+00:00"
    )
    assert (
        result["data"]["forcesExecutions"]["toDate"]
        == "2020-02-28 23:59:59+00:00"
    )
    assert executions[0]["date"] == "2020-02-05T00:00:00+00:00"
    assert executions[0]["exitCode"] == "1"
    assert executions[0]["gitBranch"] == "master"
    assert (
        executions[0]["gitCommit"]
        == "6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6"
    )
    # FP: local testing
    assert executions[0]["gitOrigin"] == "http://test.com"  # NOSONAR
    assert executions[0]["gitRepo"] == "Repository"
    assert executions[0]["kind"] == "dynamic"
    assert executions[0]["strictness"] == "strict"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("forces_executions")
@pytest.mark.parametrize(
    ["email"],
    [
        ["service_forces@gmail.com"],
    ],
)
async def test_get_forces_executions_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
