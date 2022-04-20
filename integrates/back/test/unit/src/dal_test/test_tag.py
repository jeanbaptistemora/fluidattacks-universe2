# pylint: disable=unnecessary-comprehension
from decimal import (
    Decimal,
)
import pytest
from tags.dal import (
    get_attributes,
    update,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_update() -> None:
    # company, tag, data
    test_1 = (
        "okada",
        "test-groups",
        {
            "mean_remediate_critical_severity": None,
            "mean_remediate": None,
            "max_severity": Decimal("3.3"),
        },
    )
    original = {
        "mean_remediate_critical_severity": Decimal("0"),
        "mean_remediate": Decimal("687"),
        "max_severity": Decimal("6.3"),
    }
    attributes = [attr for attr in original]
    assert original == await get_attributes(test_1[0], test_1[1], attributes)
    assert await update(*test_1)
    assert {"max_severity": Decimal("3.3")} == await get_attributes(
        test_1[0], test_1[1], attributes
    )
