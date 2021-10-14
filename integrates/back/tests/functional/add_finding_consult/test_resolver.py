from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
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
    ],
)
async def test_add_finding_consultant(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        content="This is a observation test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        mutation_type="CONSULT",
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["resourcer@gmail.com"],
    ],
)
async def test_add_finding_consultant_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        content="This is a observation test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        mutation_type="CONSULT",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_add_finding_consult_without_squad(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        content="This is a consulting test",
        finding="697510163",
        mutation_type="CONSULT",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_finding_observation_without_squad(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        content="This is a observation test",
        finding="697510163",
        mutation_type="OBSERVATION",
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]
