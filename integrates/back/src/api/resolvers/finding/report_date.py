# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    convert_from_iso_str,
)
from typing import (
    Optional,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[str]:
    unreliable_indicators = parent.unreliable_indicators
    if unreliable_indicators.unreliable_oldest_vulnerability_report_date:
        return convert_from_iso_str(
            unreliable_indicators.unreliable_oldest_vulnerability_report_date
        )
    if parent.creation:
        return convert_from_iso_str(parent.creation.modified_date)
    return None
