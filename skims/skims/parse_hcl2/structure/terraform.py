from collections.abc import (
    Iterator,
)
from parse_hcl2.common import (
    iterate_resources,
)
from typing import (
    Any,
    NamedTuple,
)


class TerraformSettings(NamedTuple):
    column: int
    data: list[Any]
    line: int


def iter_terraform_settings(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "terraform", None)
    for bucket in iterator:
        yield TerraformSettings(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )
