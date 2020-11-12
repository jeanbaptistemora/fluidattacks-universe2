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
    yield_nodes_with_key,
)


def yield_normal_class(
    model: Dict[str, Any],
) -> Iterator[Dict[str, Any]]:
    # *.NormalClassDeclaration
    for node in yield_nodes_with_key(key='NormalClassDeclaration', node=model):
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


def yield_normal_class_methods(
    model: Dict[str, Any],
) -> Iterator[Dict[str, Any]]:
    # *.NormalClassDeclaration
    # .ClassBody[*].ClassBodyDeclaration.ClassMemberDeclaration
    # .MethodDeclaration

    # pylint: disable=too-many-nested-blocks
    for normal_class_declaration in yield_normal_class(model):
        body = (
            normal_class_declaration
            ['NormalClassDeclaration']
            ['ClassBody']
        )
        if isinstance(body, list):
            for body_element in body[1:-1]:
                if 'ClassBodyDeclaration' in body_element:
                    declaration = body_element['ClassBodyDeclaration'][0]

                    if 'ClassMemberDeclaration' in declaration:
                        body = declaration['ClassMemberDeclaration'][0]

                        if 'MethodDeclaration' in body:
                            yield {
                                'MethodDeclaration': parse_rule(
                                    body['MethodDeclaration'],
                                    {
                                        'MethodModifier': [],
                                        'MethodHeader': None,
                                        'MethodBody': None,
                                    },
                                ),
                            }
