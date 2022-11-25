from dataloaders import (
    Dataloaders,
)
from db_model.companies.types import (
    Company,
    Trial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Optional,
)


async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Company]:
    loaders: Dataloaders = info.context.loaders
    domain = str(parent["user_email"]).split("@")[1]
    company: Optional[Company] = await loaders.company.load(domain)

    if company:
        return company

    return Company(
        domain=domain,
        trial=Trial(
            completed=False,
            extension_date="",
            extension_days=0,
            start_date="",
        ),
    )
