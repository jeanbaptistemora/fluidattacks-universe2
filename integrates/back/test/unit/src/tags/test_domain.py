from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.portfolios.types import (
    Portfolio,
    PortfolioRequest,
    PortfolioUnreliableIndicators,
)
from decimal import (
    Decimal,
)
import pytest
from tags import (
    domain as tags_domain,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_update() -> None:
    loaders: Dataloaders = get_new_context()
    original: Portfolio = await loaders.portfolio.load(
        PortfolioRequest(organization_name="okada", portfolio_id="test-groups")
    )
    # company, tag, data
    test_1 = Portfolio(
        id=original.id,
        groups=original.groups,
        organization_name=original.organization_name,
        unreliable_indicators=PortfolioUnreliableIndicators(
            max_open_severity=original.unreliable_indicators.max_open_severity,
            max_severity=Decimal("3.3"),
            mean_remediate=original.unreliable_indicators.mean_remediate,
            mean_remediate_critical_severity=Decimal("1.5"),
            mean_remediate_high_severity=Decimal("0"),
            mean_remediate_low_severity=Decimal("5.3"),
            mean_remediate_medium_severity=Decimal("0"),
            last_closing_date=original.unreliable_indicators.last_closing_date,
        ),
    )
    assert original.unreliable_indicators.max_severity == Decimal("6.3")
    assert original.unreliable_indicators.mean_remediate == Decimal("688")
    assert original.unreliable_indicators.mean_remediate_critical_severity == (
        Decimal("0")
    )

    await tags_domain.update(portfolio=test_1)
    loaders = get_new_context()
    updated: Portfolio = await loaders.portfolio.load(
        PortfolioRequest(organization_name="okada", portfolio_id="test-groups")
    )
    assert updated.unreliable_indicators.mean_remediate_critical_severity == (
        Decimal("1.5")
    )
    assert updated.unreliable_indicators.mean_remediate_low_severity == (
        Decimal("5.3")
    )
    assert updated.unreliable_indicators.mean_remediate_medium_severity == (
        Decimal("0")
    )
    assert updated.unreliable_indicators.mean_remediate_high_severity == (
        Decimal("0")
    )
    assert updated.unreliable_indicators.max_severity == (Decimal("3.3"))
