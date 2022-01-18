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
