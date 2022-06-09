from .types import (
    Portfolio,
    PortfolioUnreliableIndicators,
)
from dynamodb.types import (
    Item,
)


def format_unreliable_indicators(item: Item) -> PortfolioUnreliableIndicators:
    return PortfolioUnreliableIndicators(
        last_closing_date=int(item["last_closing_date"])
        if "last_closing_date" in item
        else None,
        max_open_severity=item.get("max_open_severity"),
        max_severity=item.get("max_severity"),
        mean_remediate=item.get("mean_remediate"),
        mean_remediate_critical_severity=item.get(
            "mean_remediate_critical_severity"
        ),
        mean_remediate_high_severity=item.get("mean_remediate_high_severity"),
        mean_remediate_low_severity=item.get("mean_remediate_low_severity"),
        mean_remediate_medium_severity=item.get(
            "mean_remediate_medium_severity"
        ),
    )


def format_portfolio(item: Item) -> Portfolio:
    return Portfolio(
        id=item["id"],
        groups=set(item["groups"]),
        organization_name=item["organization_name"],
        unreliable_indicators=format_unreliable_indicators(
            item["unreliable_indicators"]
        ),
    )


def format_portfolio_item(portfolio: Portfolio) -> Item:
    return {
        "id": portfolio.id,
        "organization_name": portfolio.organization_name,
        "groups": list(portfolio.groups),
        "unreliable_indicators": portfolio.unreliable_indicators._asdict(),
    }
