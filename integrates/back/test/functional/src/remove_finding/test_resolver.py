from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_finding")
@pytest.mark.parametrize(
    ["email", "finding_id"],
    [
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
    ],
)
async def test_remove_finding(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeFinding"]
    assert result["data"]["removeFinding"]["success"]

    loaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.state.status == FindingStateStatus.DELETED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_finding")
@pytest.mark.parametrize(
    ["email", "finding_id"],
    [
        ["hacker@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
        ["reattacker@gmail.com", "475041520"],
    ],
)
async def test_remove_finding_fail(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
