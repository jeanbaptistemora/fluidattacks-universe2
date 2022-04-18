from custom_types import (
    Me,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.vulnerabilities import (
    filter_non_zero_risk,
    filter_open_vulns,
)
from typing import (
    Tuple,
)


async def resolve(
    parent: Me, info: GraphQLResolveInfo
) -> Tuple[Vulnerability, ...]:
    email: str = str(parent["user_email"])
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await info.context.loaders.me_vulnerabilities.load(email)

    return filter_non_zero_risk(filter_open_vulns(vulnerabilities))
