# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Union,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Union[Finding20Severity, Finding31Severity]:
    return parent.severity
