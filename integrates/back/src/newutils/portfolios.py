from db_model.portfolios.types import (
    Portfolio,
    PortfolioUnreliableIndicators,
)
from dynamodb.types import (
    Item,
)
from newutils.utils import (
    get_key_or_fallback,
)


def format_unreliable_indicators(
    item: Item,
) -> PortfolioUnreliableIndicators:
    return PortfolioUnreliableIndicators(
        last_closing_date=get_key_or_fallback(
            item, "last_closing_date", "last_closed_vulnerability_days"
        ),
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


def format_portfolio(
    item: Item,
) -> Portfolio:
    return Portfolio(
        id=get_key_or_fallback(item, "id", "tag"),
        groups=get_key_or_fallback(item, "groups", "projects", set()),
        unreliable_indicators=format_unreliable_indicators(item),
        organization_name=get_key_or_fallback(
            item,
            "organization_id",
            "organization",
        ),
    )
