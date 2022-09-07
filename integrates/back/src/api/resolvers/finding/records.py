# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> list[dict[object, object]]:
    records = []
    if parent.evidences.records:
        records = await findings_domain.get_records_from_file(
            parent.group_name, parent.id, parent.evidences.records.url
        )

    return records
