# Standard library
from typing import (
    Any,
    Iterator,
)

# Third party libraries
from lark import (
    Tree,
)

# Local libraries
from parse_hcl2.tokens import (
    Block,
)


def iterate_resources(
    model: Any,
    expected_source: str,
    *expected_kinds: str,
) -> Iterator[Block]:
    if isinstance(model, Tree):
        for child in model.children:
            yield from iterate_resources(
                child,
                expected_source,
                *expected_kinds,
            )
    elif isinstance(model, Block) and (
        len(model.namespace) == 3
        and model.namespace[0] == expected_source
        and model.namespace[1] in expected_kinds
    ):
        yield model
