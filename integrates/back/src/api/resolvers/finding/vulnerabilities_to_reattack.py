from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from findings.domain import (
    get_vulnerabilities_to_reattack,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Vulnerability]:
    return list(
        await get_vulnerabilities_to_reattack(
            loaders=info.context.loaders,
            finding_id=parent.id,
        )
    )
