from dataloaders import (
    Dataloaders,
)
from db_model.companies.types import (
    Company,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Company]:
    loaders: Dataloaders = info.context.loaders
    domain = parent.created_by.split("@")[1]
    company: Optional[Company] = await loaders.company.load(domain)

    return company
