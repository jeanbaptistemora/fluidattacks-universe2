from . import (
    get_result,
    get_stakeholder_organizations,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("unsubscribe_from_group")
@pytest.mark.parametrize(
    ["email", "stakeholder_groups", "to_be_removed"],
    [
        ["admin@gmail.com", 0, True],
        ["hacker@gmail.com", 2, False],
        ["reattacker@gmail.com", 1, True],
        ["user@gmail.com", 1, True],
        ["resourcer@gmail.com", 1, True],
        ["reviewer@gmail.com", 2, False],
    ],
)
async def test_unsubscribe_from_group(
    populate: bool, email: str, stakeholder_groups: bool, to_be_removed: bool
) -> None:
    assert populate
    result: dict[str, Any] = await get_stakeholder_organizations(
        email=email,
    )
    assert "errors" not in result
    assert len(result["data"]["me"]["organizations"]) == 1
    assert (
        len(result["data"]["me"]["organizations"][0]["groups"])
        == stakeholder_groups
    )

    result = await get_result(
        email=email,
        group_name="group1",
    )
    assert "errors" not in result
    assert result["data"]["unsubscribeFromGroup"]["success"]

    loaders: Dataloaders = get_new_context()
    if to_be_removed:
        assert not await loaders.stakeholder.load(email)
    else:
        assert await loaders.stakeholder.load(email)

    result = await get_stakeholder_organizations(
        email=email,
    )
    assert "errors" not in result
    if stakeholder_groups in [0, 1]:
        assert len(result["data"]["me"]["organizations"]) == 0
    else:
        assert (
            len(result["data"]["me"]["organizations"][0]["groups"])
            == stakeholder_groups - 1
        )
