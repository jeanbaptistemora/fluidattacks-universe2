from . import (
    get_result,
)
import logging
import pytest
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("forces_executions_s3")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_forces_executions(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    executions = result["data"]["group"]["executionsConnections"]["edges"]
    assert executions[0]["node"]["date"] == "2020-02-05T00:00:00+00:00"
    assert executions[0]["node"]["exitCode"] == "1"
    assert executions[0]["node"]["gitBranch"] == "master"
    assert (
        executions[0]["node"]["gitCommit"]
        == "6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6"
    )
    # FP: local testing
    assert executions[0]["node"]["gitOrigin"] == "http://test.com"  # NOSONAR
    assert executions[0]["node"]["gitRepo"] == "Repository"
    assert executions[0]["node"]["kind"] == "dynamic"
    assert executions[0]["node"]["strictness"] == "strict"
    assert executions[0]["node"]["gracePeriod"] == 0
    assert executions[0]["node"]["severityThreshold"] == 0.0


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("forces_executions_s3")
@pytest.mark.parametrize(
    ["email"],
    [
        ["service_forces@gmail.com"],
    ],
)
async def test_get_forces_executions_fail(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
