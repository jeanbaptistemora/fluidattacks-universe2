# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    fields,
)
from typing import (
    Any,
    Tuple,
)


def format_query_fields(table_row_class: Any) -> Tuple[str, str]:
    _fields = ",".join(tuple(f.name for f in fields(table_row_class)))
    values = ",".join(tuple(f"%({f.name})s" for f in fields(table_row_class)))
    return _fields, values


def get_query_fields(table_row_class: Any) -> list[str]:
    return list(f.name for f in fields(table_row_class))
