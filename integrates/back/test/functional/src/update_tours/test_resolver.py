from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_tours")
@pytest.mark.parametrize(
    ("email", "tours"),
    (
        (
            "admin@gmail.com",
            {"newGroup": "true", "newRiskExposure": "true", "newRoot": "true"},
        ),
    ),
)
async def test_update_tours(
    populate: bool,
    email: str,
    tours: Dict[str, bool],
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        tours=tours,
    )
    assert "errors" not in result
    assert result["data"]["updateTours"]["success"]
    loaders: Dataloaders = get_new_context()
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder.tours.new_group is True
    assert stakeholder.tours.new_risk_exposure is True
    assert stakeholder.tours.new_root is True
