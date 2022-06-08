from .types import (
    Portfolio,
)
from dynamodb.types import (
    Item,
)


def format_portfolio_item(portfolio: Portfolio) -> Item:
    return {
        "id": portfolio.id,
        "organization_name": portfolio.organization_name,
        "groups": list(portfolio.groups),
        "unreliable_indicators": portfolio.unreliable_indicators._asdict(),
    }
