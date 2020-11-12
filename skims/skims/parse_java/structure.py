# Standard library
from typing import (
    Any,
    Dict,
    Iterator,
)

# Local libraries
from parse_antlr import (
    parse_rule,
)
from utils.graph import (
    yield_nodes,
)


def yield_normal_class_declaration(
    model: Dict[str, Any],
) -> Iterator[Dict[str, Any]]:
    for node in yield_nodes(
        key_predicates=(
            'NormalClassDeclaration'.__eq__,
        ),
        post_extraction=(),
        pre_extraction=(),
        value=model,
    ):
        yield {
            'NormalClassDeclaration': parse_rule(node, {
                'ClassModifier': [],
                '__token__.0': None,
                'Identifier': None,
                'TypeParameters': None,
                'Superclass': None,
                'Superinterfaces': None,
                'ClassBody': None,
            }),
        }
