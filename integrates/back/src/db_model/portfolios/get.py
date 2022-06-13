from .types import (
    Portfolio,
)
from .utils import (
    format_portfolio,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    PortfolioNotFound,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_organization_portfolios(
    organization_name: str,
) -> tuple[Portfolio, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["portfolio_metadata"],
        values={"name": organization_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["portfolio_metadata"],),
        table=TABLE,
        index=index,
    )

    return tuple(format_portfolio(item) for item in response.items)


async def _get_portfolio(
    *,
    organization_name: str,
    portfolio_id: str,
) -> Portfolio:
    organization_name = organization_name.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["portfolio_metadata"],
        values={
            "id": portfolio_id,
            "name": organization_name,
        },
    )
    item = await operations.get_item(
        facets=(TABLE.facets["portfolio_metadata"],),
        key=primary_key,
        table=TABLE,
    )
    if not item:
        raise PortfolioNotFound.new()

    return format_portfolio(item)


class OrganizationPortfoliosLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_names: Iterable[str]
    ) -> tuple[tuple[Portfolio, ...], ...]:
        return await collect(
            tuple(map(_get_organization_portfolios, organization_names))
        )


class PortfolioLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self,
        portfolio_keys: Iterable[tuple[str, str]],
    ) -> tuple[Portfolio, ...]:
        # This loaders receives a tuple with (organization_name, portfolio_id)
        return await collect(
            tuple(
                _get_portfolio(
                    organization_name=organization_name,
                    portfolio_id=portfolio_id,
                )
                for organization_name, portfolio_id in portfolio_keys
            )
        )
