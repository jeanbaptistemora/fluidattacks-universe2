from . import (
    get_result,
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
@pytest.mark.resolver_test_group("update_tours")
@pytest.mark.parametrize(
    ("email", "tours"),
    (
        (
            "admin@gmail.com",
            {
                "newGroup": "true",
                "newRiskExposure": "true",
                "newRoot": "true",
                "welcome": "true",
            },
        ),
    ),
)
async def test_update_tours(
    populate: bool,
    email: str,
    tours: dict[str, bool],
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        tours=tours,
    )
    assert "errors" not in result
    assert result["data"]["updateTours"]["success"]
    loaders: Dataloaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert stakeholder.tours.new_group is True
    assert stakeholder.tours.new_risk_exposure is True
    assert stakeholder.tours.new_root is True
    assert stakeholder.tours.welcome is True
