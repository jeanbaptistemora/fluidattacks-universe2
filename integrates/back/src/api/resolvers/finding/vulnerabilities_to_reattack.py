from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.vulnerabilities import (
    filter_open_vulns_new,
    filter_remediated,
)
from typing import (
    List,
    Tuple,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Vulnerability]:
    finding_vulns_loader = info.context.loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability] = await finding_vulns_loader.load(parent.id)
    return list(filter_open_vulns_new(filter_remediated(vulns)))
