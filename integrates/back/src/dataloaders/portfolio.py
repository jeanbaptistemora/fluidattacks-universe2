from aiodataloader import (
    DataLoader,
)
from db_model.portfolios.types import (
    Portfolio,
)
from dynamodb.types import (
    Item,
)
from newutils.portfolios import (
    format_portfolio,
)
from tags import (
    dal,
)
from typing import (
    Iterable,
)


class OrganizationPortfoliosTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_names: Iterable[str]
    ) -> tuple[tuple[Portfolio, ...], ...]:
        orgs_portfolio_items: list[list[Item]] = [
            await dal.get_tags(name, None) for name in organization_names
        ]
        return tuple(
            tuple(format_portfolio(item) for item in portfolio_items)
            for portfolio_items in orgs_portfolio_items
        )


class PortfolioTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self,
        keys: Iterable[tuple[str, str]],
    ) -> tuple[Portfolio, ...]:
        orgs_portfolio_items = [
            await dal.get_attributes(name, tag_id) for name, tag_id in keys
        ]
        return tuple(format_portfolio(item) for item in orgs_portfolio_items)
