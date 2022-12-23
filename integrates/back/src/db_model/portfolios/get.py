from .types import (
    Portfolio,
    PortfolioRequest,
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
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
    Union,
)


async def _get_organization_portfolios(
    *,
    organization_name: str,
    portfolio_dataloader: DataLoader,
) -> tuple[Portfolio, ...]:
    organization_name = organization_name.lower().strip()
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

    portfolio_list: list[Portfolio] = []
    for item in response.items:
        portfolio = format_portfolio(item)
        portfolio_list.append(portfolio)
        portfolio_dataloader.prime(
            PortfolioRequest(
                organization_name=portfolio.organization_name,
                portfolio_id=portfolio.id,
            ),
            portfolio,
        )

    return tuple(portfolio_list)


async def _get_portfolios(
    *, requests: tuple[PortfolioRequest, ...]
) -> Union[tuple[Portfolio, ...], None]:
    requests = tuple(
        request._replace(
            organization_name=request.organization_name.lower().strip()
        )
        for request in requests
    )
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["portfolio_metadata"],
            values={
                "id": request.portfolio_id,
                "name": request.organization_name,
            },
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    if len(items) == len(requests):
        response = {
            PortfolioRequest(
                organization_name=portfolio.organization_name,
                portfolio_id=portfolio.id,
            ): portfolio
            for portfolio in tuple(format_portfolio(item) for item in items)
        }
        return tuple(response[request] for request in requests)

    return None


class OrganizationPortfoliosLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_names: Iterable[str]
    ) -> tuple[tuple[Portfolio, ...], ...]:
        return await collect(
            tuple(
                _get_organization_portfolios(
                    organization_name=organization_name,
                    portfolio_dataloader=self.dataloader,
                )
                for organization_name in organization_names
            )
        )


class PortfolioLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: Iterable[PortfolioRequest]
    ) -> Union[tuple[Portfolio, ...], None]:
        return await _get_portfolios(requests=tuple(requests))
