from db_model.portfolios.constants import (
    GROUPS,
    ID,
    LAST_CLOSING_DATE,
    MAX_OPEN_SEVERITY,
    MAX_SEVERITY,
    MEAN_REMED_CRITICAL_SEV,
    MEAN_REMED_HIGH_SEV,
    MEAN_REMED_LOW_SEV,
    MEAN_REMED_MEDIUM_SEV,
    MEAN_REMEDIATE,
    OLD_GROUPS,
    OLD_ID,
    OLD_ORGANIZATION_ID,
    ORGANIZATION_ID,
    UNRELIABLE_INDICATORS,
)
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
        last_closing_date=item[LAST_CLOSING_DATE],
        max_open_severity=item[MAX_OPEN_SEVERITY],
        max_severity=item[MAX_SEVERITY],
        mean_remediate=item[MEAN_REMEDIATE],
        mean_remediate_critical_severity=item[MEAN_REMED_CRITICAL_SEV],
        mean_remediate_high_severity=item[MEAN_REMED_HIGH_SEV],
        mean_remediate_low_severity=item[MEAN_REMED_LOW_SEV],
        mean_remediate_medium_severity=item[MEAN_REMED_MEDIUM_SEV],
    )


def format_portfolio(
    item: Item,
) -> Portfolio:
    return Portfolio(
        id=get_key_or_fallback(item, ID, OLD_ID),
        groups=get_key_or_fallback(item, GROUPS, OLD_GROUPS),
        unreliable_indicators=format_unreliable_indicators(
            get_key_or_fallback(
                item,
                UNRELIABLE_INDICATORS,
            ),
        ),
        organization_id=get_key_or_fallback(
            item,
            ORGANIZATION_ID,
            OLD_ORGANIZATION_ID,
        ),
    )
