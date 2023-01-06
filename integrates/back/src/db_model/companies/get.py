from .types import (
    Company,
)
from .utils import (
    format_company,
)
from aiodataloader import (
    DataLoader,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Optional,
)


async def _get_companies(domains: list[str]) -> tuple[Company, ...]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["company_metadata"],
            values={"domain": domain},
        )
        for domain in domains
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)
    return tuple(format_company(item) for item in items)


class CompanyLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, domains: list[str]
    ) -> tuple[Optional[Company], ...]:
        companies = {
            company.domain: company
            for company in await _get_companies(domains)
        }
        return tuple(companies.get(domain) for domain in domains)
