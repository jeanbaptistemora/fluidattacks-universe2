from custom_types import (
    Me as MeType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.token import (
    get_jwt_content,
)
from newutils.vulnerabilities import (
    filter_non_zero_risk,
    filter_open_vulns,
)
from typing import (
    Tuple,
)


async def resolve(
    _parent: MeType, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Vulnerability, ...]:
    user_data = await get_jwt_content(info.context)
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await info.context.loaders.me_vulnerabilities.load(
        user_data["user_email"]
    )

    return filter_non_zero_risk(filter_open_vulns(vulnerabilities))
