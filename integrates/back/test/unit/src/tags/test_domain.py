from custom_exceptions import (
    PortfolioNotFound,
)
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
from tags.domain import (
    remove,
    update,
)
from typing import (
    Optional,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]

MODULE_AT_TEST = "tags.domain."


@pytest.mark.parametrize(
    ["organization_name", "portfolio_id"],
    [
        ["okada", "test-groups"],
    ],
)
@patch(MODULE_AT_TEST + "portfolios_model.remove", new_callable=AsyncMock)
async def test_remove(
    mock_portfolios_model: AsyncMock,
    organization_name: str,
    portfolio_id: str,
) -> None:

    mock_portfolios_model.return_value = None
    await remove(
        organization_name=organization_name, portfolio_id=portfolio_id
    )
    assert mock_portfolios_model.called is True
    mock_portfolios_model.assert_called_with(
        organization_name=organization_name, portfolio_id=portfolio_id
    )


@pytest.mark.changes_db
async def test_update() -> None:
    loaders: Dataloaders = get_new_context()
    original: Optional[Portfolio] = await loaders.portfolio.load(
        PortfolioRequest(organization_name="okada", portfolio_id="test-groups")
    )
    if original:
        # company, tag, data
        test_1 = Portfolio(
            id=original.id,
            groups=original.groups,
            organization_name=original.organization_name,
            unreliable_indicators=PortfolioUnreliableIndicators(
                max_open_severity=(
                    original.unreliable_indicators.max_open_severity
                ),
                max_severity=Decimal("3.3"),
                mean_remediate=original.unreliable_indicators.mean_remediate,
                mean_remediate_critical_severity=Decimal("1.5"),
                mean_remediate_high_severity=Decimal("0"),
                mean_remediate_low_severity=Decimal("5.3"),
                mean_remediate_medium_severity=Decimal("0"),
                last_closing_date=(
                    original.unreliable_indicators.last_closing_date
                ),
            ),
        )
        assert original.unreliable_indicators.max_severity == Decimal("6.3")
        assert original.unreliable_indicators.mean_remediate == Decimal("688")
        assert (
            original.unreliable_indicators.mean_remediate_critical_severity
            == (Decimal("0"))
        )
        await update(portfolio=test_1)
    else:
        raise PortfolioNotFound()

    loaders = get_new_context()
    updated: Optional[Portfolio] = await loaders.portfolio.load(
        PortfolioRequest(organization_name="okada", portfolio_id="test-groups")
    )
    if updated:
        assert (
            updated.unreliable_indicators.mean_remediate_critical_severity
            == (Decimal("1.5"))
        )
        assert updated.unreliable_indicators.mean_remediate_low_severity == (
            Decimal("5.3")
        )
        assert (
            updated.unreliable_indicators.mean_remediate_medium_severity
            == (Decimal("0"))
        )
        assert updated.unreliable_indicators.mean_remediate_high_severity == (
            Decimal("0")
        )
        assert updated.unreliable_indicators.max_severity == (Decimal("3.3"))
    else:
        raise PortfolioNotFound()
