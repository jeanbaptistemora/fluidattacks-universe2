from dataloaders import (
    Dataloaders,
    get_new_context,
)
from groups.domain import (
    get_closed_vulnerabilities,
    get_open_findings,
    get_open_vulnerabilities,
    get_vulnerabilities_with_pending_attacks,
    is_valid,
    validate_group_tags,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_validate_tags() -> None:
    loaders: Dataloaders = get_new_context()
    assert await validate_group_tags(
        loaders, "unittesting", ["testtag", "this-is-ok", "th15-4l50"]
    )
    assert await validate_group_tags(
        loaders, "unittesting", ["this-tag-is-valid", "but this is not"]
    ) == ["this-tag-is-valid"]


async def test_is_valid() -> None:
    loaders: Dataloaders = get_new_context()
    assert await is_valid(loaders, "unittesting")
    assert not await is_valid(loaders, "nonexistent_group")


async def test_get_vulnerabilities_with_pending_attacks() -> None:
    context = get_new_context()
    test_data = await get_vulnerabilities_with_pending_attacks(
        loaders=context, group_name="unittesting"
    )
    expected_output = 1
    assert test_data == expected_output


async def test_get_open_vulnerabilities() -> None:
    group_name = "unittesting"
    expected_output = 29
    open_vulns = await get_open_vulnerabilities(get_new_context(), group_name)
    assert open_vulns == expected_output


async def test_get_closed_vulnerabilities() -> None:
    group_name = "unittesting"
    expected_output = 7
    closed_vulnerabilities = await get_closed_vulnerabilities(
        get_new_context(), group_name
    )
    assert closed_vulnerabilities == expected_output


async def test_get_open_findings() -> None:
    group_name = "unittesting"
    expected_output = 5
    open_findings = await get_open_findings(get_new_context(), group_name)
    assert open_findings == expected_output
