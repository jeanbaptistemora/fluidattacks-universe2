from custom_types import (
    Vulnerability as VulnerabilityType,
)
from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    vulnerabilities as vulns_utils,
)
from roots.types import (
    Root,
)
from typing import (
    List,
)


async def resolve(
    parent: Root, info: GraphQLResolveInfo, **_kwargs: None
) -> List[VulnerabilityType]:
    loaders: Dataloaders = info.context.loaders
    root_vulns = await vulns_utils.filter_vulns_by_nickname(
        loaders, parent.group_name, parent.nickname
    )

    return root_vulns
