# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    OrgFindingPolicy,
    OrgFindingPolicyState,
)
from db_model import (
    TABLE,
)
from dynamodb.types import (
    Item,
)


def format_organization_finding_policy(
    item: Item,
) -> OrgFindingPolicy:
    key_structure = TABLE.primary_key
    return OrgFindingPolicy(
        id=item[key_structure.partition_key].split("#")[1],
        name=item["name"],
        organization_name=item[key_structure.sort_key].split("#")[1],
        state=OrgFindingPolicyState(
            modified_by=item["state"]["modified_by"],
            modified_date=item["state"]["modified_date"],
            status=item["state"]["status"],
        ),
        tags=item.get("tags", {}),
    )
