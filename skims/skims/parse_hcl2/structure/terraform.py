from parse_hcl2.common import (
    iterate_resources,
)
from typing import (
    Any,
    Iterator,
    List,
    NamedTuple,
)


class TerraformSettings(NamedTuple):
    column: int
    data: List[Any]
    line: int


def iter_terraform_settings(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "terraform", None)
    for bucket in iterator:
        yield TerraformSettings(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )
