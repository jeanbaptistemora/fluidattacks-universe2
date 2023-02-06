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
    Optional,
)


async def _get_organization_portfolios(
    *,
    organization_name: str,
    portfolio_dataloader: DataLoader,
) -> list[Portfolio]:
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

    return portfolio_list


async def _get_portfolios(
    *, requests: Iterable[PortfolioRequest]
) -> list[Optional[Portfolio]]:
    requests_formatted = list(
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
        for request in requests_formatted
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    response = {
        PortfolioRequest(
            organization_name=portfolio.organization_name,
            portfolio_id=portfolio.id,
        ): portfolio
        for portfolio in [format_portfolio(item) for item in items]
    }

    return [response.get(request) for request in requests_formatted]


class OrganizationPortfoliosLoader(DataLoader[str, list[Portfolio]]):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_names: Iterable[str]
    ) -> list[list[Portfolio]]:
        return list(
            await collect(
                _get_organization_portfolios(
                    organization_name=organization_name,
                    portfolio_dataloader=self.dataloader,
                )
                for organization_name in organization_names
            )
        )


class PortfolioLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[PortfolioRequest]
    ) -> list[Optional[Portfolio]]:
        return await _get_portfolios(requests=requests)
