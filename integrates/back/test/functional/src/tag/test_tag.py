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
)
import pytest
from typing import (
    Optional,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("tag")
async def test_get_tag(populate: bool) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    tag: Optional[Portfolio] = await loaders.portfolio.load(
        PortfolioRequest(organization_name="orgtest", portfolio_id="test-tag")
    )
    if tag:
        assert tag.unreliable_indicators.last_closing_date == 50
        assert tag.unreliable_indicators.mean_remediate_critical_severity == 0
        assert tag.unreliable_indicators.mean_remediate_high_severity == 0
        assert tag.unreliable_indicators.mean_remediate_low_severity == 116
        assert tag.unreliable_indicators.mean_remediate_medium_severity == 135
        assert tag.unreliable_indicators.mean_remediate == 123
    else:
        raise PortfolioNotFound()
