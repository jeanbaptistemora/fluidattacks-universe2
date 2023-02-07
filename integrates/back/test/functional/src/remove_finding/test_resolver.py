# pylint: disable=import-error
from . import (
    get_result,
)
from back.test.functional.src.finding import (
    get_result as get_finding,
)
from back.test.functional.src.group import (
    get_result as get_group,
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

    result = await get_group(user=email, group=finding.group_name)
    assert finding_id not in [
        finding["id"] for finding in result["data"]["group"]["findings"]
    ]

    result = await get_finding(user=email, finding_id=finding_id)
    assert result["data"]["finding"]["currentState"] == "DELETED"


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
