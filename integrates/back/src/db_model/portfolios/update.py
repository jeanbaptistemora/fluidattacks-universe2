from .types import (
    Portfolio,
)
from .utils import (
    format_portfolio_item,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def update(
    *,
    portfolio: Portfolio,
) -> None:
    portfolio_key = keys.build_key(
        facet=TABLE.facets["portfolio_metadata"],
        values={
            "id": portfolio.id,
            "name": portfolio.organization_name,
        },
    )
    portfolio_item = format_portfolio_item(portfolio)
    await operations.update_item(
        item=portfolio_item,
        key=portfolio_key,
        table=TABLE,
    )
