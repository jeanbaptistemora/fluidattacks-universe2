# Standard library
import ast
from typing import (
    Callable,
    cast,
    Iterator,
    Tuple,
    TypeVar,
)

# Constants
_T = TypeVar('_T')


def parse(content: str) -> ast.AST:
    try:
        tree: ast.AST = ast.parse(content)
    except SyntaxError:
        tree = ast.Module()

    return tree


def iterate_nodes(
    content: str,
    filters: Tuple[Callable[[_T], bool], ...],
) -> Iterator[_T]:
    for _node in ast.walk(parse(content)):
        node = cast(_T, _node)
        if all(f(node) for f in filters):
            yield node
