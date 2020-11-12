# Standard library
from typing import (
    Any,
    Dict,
    Iterator,
)

# Local libraries
from utils.graph import (
    yield_nodes_with_key,
)


def yield_normal_class(model: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    # *.NormalClassDeclaration
    for node in yield_nodes_with_key(key='NormalClassDeclaration', node=model):
        yield node


def yield_normal_class_methods(
    model: Dict[str, Any],
) -> Iterator[Dict[str, Any]]:
    # *.NormalClassDeclaration
    # .ClassBody.ClassBodyDeclaration.ClassMemberDeclaration.MethodDeclaration

    for normal_class in yield_normal_class(model):
        if decs := normal_class['ClassBody'].get('ClassBodyDeclaration'):
            for declaration in decs:
                if member := declaration.get('ClassMemberDeclaration'):
                    if method := member.get('MethodDeclaration'):
                        yield method
