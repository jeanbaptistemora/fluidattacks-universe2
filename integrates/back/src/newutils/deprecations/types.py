# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from typing import (
    NamedTuple,
)


class ApiFieldType(Enum):
    DIRECTIVE = "directive_definition"
    ENUM = "enum_type_definition"
    INPUT = "input_object_type_definition"
    OBJECT = "object_type_definition"


class ApiDeprecation(NamedTuple):
    parent: str
    field: str
    reason: str
    due_date: datetime
    type: ApiFieldType
