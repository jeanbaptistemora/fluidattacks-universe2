# Standard library
import ast
from typing import (
    Optional,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from frozendict import (
    frozendict
)
import lark


# Constants
GRAMMAR = r"""
    ?start: value

    ?value: object
            | array
            | string
            | SIGNED_NUMBER      -> number
            | "true"             -> true
            | "false"            -> false
            | "null"             -> null

    array  : "[" [value ("," value)*] "]"
    object : "{" [pair ("," pair)*] "}"
    pair   : string ":" value

    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS

    %ignore WS
"""


def blocking_loads(
    stream: str,
    *,
    default: Optional[frozendict] = None,
) -> frozendict:
    json_parser = lark.Lark(
        grammar=GRAMMAR,
        parser='lalr',
        lexer='standard',
        propagate_positions=True,
        maybe_placeholders=False,
        transformer=Builder(),
    )

    try:
        return json_parser.parse(stream)
    except lark.exceptions.LarkError:
        if default is None:
            raise

        return default


async def loads(
    stream: str,
    *,
    default: Optional[frozendict] = None,
) -> frozendict:
    return await in_process(blocking_loads, stream, default=default)


class Builder(lark.Transformer[frozendict]):

    pair = tuple
    object = frozendict

    @staticmethod
    @lark.v_args(inline=True)
    def string(token: lark.Token) -> frozendict:
        return frozendict({
            'column': token.column,
            'item': ast.literal_eval(token),
            'line': token.line
        })

    @staticmethod
    @lark.v_args(inline=True)
    def number(token: lark.Token) -> frozendict:
        return frozendict({
            'column': token.column,
            'item': ast.literal_eval(token),
            'line': token.line,
        })

    @staticmethod
    @lark.v_args(tree=True)
    def array(tree: lark.Tree) -> frozendict:
        return frozendict({
            'column': 0,
            'item': tuple(tree.children),
            'line': 0,
        })
