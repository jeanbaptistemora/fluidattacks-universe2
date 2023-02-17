from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("records")
async def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> list[dict[object, object]]:
    records = []
    if parent.evidences.records:
        records = await findings_domain.get_records_from_file(
            parent.group_name, parent.id, parent.evidences.records.url
        )

    return records
