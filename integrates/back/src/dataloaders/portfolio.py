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
from organizations import (
    domain as orgs_domain,
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
        self, organization_ids: Iterable[str]
    ) -> list[tuple[Portfolio, ...]]:
        org_names: list[str] = [
            await orgs_domain.get_name_by_id(org_id)
            for org_id in organization_ids
        ]
        orgs_portfolios: list[list[Item]] = [
            await dal.get_tags(org_name, None) for org_name in org_names
        ]
        return [
            tuple(
                format_portfolio(
                    item=portfolio,
                )
                for portfolio in org_portfolios
            )
            for org_portfolios in orgs_portfolios
        ]
