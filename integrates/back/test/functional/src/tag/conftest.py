# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.portfolios.types import (
    Portfolio,
    PortfolioUnreliableIndicators,
)
from decimal import (
    Decimal,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("tag")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data = {
        "portfolios": [
            {
                "portfolio": Portfolio(
                    id="test-tag",
                    groups=set("unittesting"),
                    organization_name="orgtest",
                    unreliable_indicators=PortfolioUnreliableIndicators(
                        last_closing_date=50,
                        max_open_severity=Decimal("3.3"),
                        max_severity=Decimal("4.3"),
                        mean_remediate=Decimal("123"),
                        mean_remediate_critical_severity=Decimal("0.0"),
                        mean_remediate_high_severity=Decimal("0.0"),
                        mean_remediate_low_severity=Decimal("116"),
                        mean_remediate_medium_severity=Decimal("135"),
                    ),
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
