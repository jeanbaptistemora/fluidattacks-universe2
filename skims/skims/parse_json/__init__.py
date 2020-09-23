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
            | single

    array  : "[" [value ("," value)*] "]"
    object : "{" [pair ("," pair)*] "}"
    pair   : string ":" value

    false : "false"
    true : "true"
    null : "null"
    single : false | true | null
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
        transformer=JSONBuilder(),
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


class JSONBuilder(
    lark.Transformer,  # type: ignore
):

    pair = tuple
    object = frozendict
    single_map = {
        "false": False,
        "null": None,
        "true": True,
    }

    @staticmethod
    @lark.v_args(tree=True)  # type: ignore
    def single(tree: lark.Tree) -> frozendict:
        children: lark.Tree = tree.children[0]
        return frozendict({
            'column': children.column,
            'item': JSONBuilder.single_map[children.data],
            'line': children.line,
        })

    @staticmethod
    @lark.v_args(inline=True)  # type: ignore
    def string(token: lark.Token) -> frozendict:
        return frozendict({
            'column': token.column,
            'item': ast.literal_eval(token),
            'line': token.line
        })

    @staticmethod
    @lark.v_args(inline=True)  # type: ignore
    def number(token: lark.Token) -> frozendict:
        return frozendict({
            'column': token.column,
            'item': ast.literal_eval(token),
            'line': token.line,
        })

    @staticmethod
    @lark.v_args(tree=True)  # type: ignore
    def array(tree: lark.Tree) -> frozendict:
        return frozendict({
            'column': 0,
            'item': tuple(tree.children),
            'line': 0,
        })
