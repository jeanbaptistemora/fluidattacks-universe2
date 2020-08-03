# Standard library
import ast

# Third party libraries
from frozendict import (
    frozendict
)
import lark

# Local libraries
from utils.aio import (
    unblock_cpu,
)


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


def blocking_loads(stream: str) -> frozendict:
    json_parser = lark.Lark(
        grammar=GRAMMAR,
        parser='lalr',
        lexer='standard',
        propagate_positions=True,
        maybe_placeholders=False,
        transformer=Builder(),
    )

    return json_parser.parse(stream)


async def loads(stream: str) -> frozendict:
    return await unblock_cpu(blocking_loads, stream)


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
