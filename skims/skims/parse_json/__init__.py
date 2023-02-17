from aioextensions import (
    in_process,
)
import ast
from frozendict import (
    frozendict,
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


def loads_blocking(
    stream: str,
    *,
    default: frozendict | None = None,
) -> frozendict:
    json_parser = lark.Lark(
        grammar=GRAMMAR,
        parser="lalr",
        lexer="standard",
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
    default: frozendict | None = None,
) -> frozendict:
    return await in_process(loads_blocking, stream, default=default)


class JSONBuilder(lark.Transformer):

    pair = tuple
    object = frozendict
    single_map = {
        "false": False,
        "null": None,
        "true": True,
    }

    @staticmethod
    @lark.v_args(tree=True)
    def single(tree: lark.Tree) -> frozendict:
        children: lark.Tree = tree.children[0]
        return frozendict(
            {
                "column": children.column,
                "item": JSONBuilder.single_map[children.data],
                "line": children.line,
            }
        )

    @staticmethod
    @lark.v_args(inline=True)
    def string(token: lark.Token) -> frozendict:
        return frozendict(
            {
                "column": token.column,
                "item": ast.literal_eval(token),
                "line": token.line,
            }
        )

    @staticmethod
    @lark.v_args(inline=True)
    # Exception: WF(Cannot factorize function)
    def number(token: lark.Token) -> frozendict:  # NOSONAR
        return frozendict(
            {
                "column": token.column,
                "item": ast.literal_eval(token),
                "line": token.line,
            }
        )

    @staticmethod
    @lark.v_args(tree=True)
    def array(tree: lark.Tree) -> frozendict:
        return frozendict(
            {
                "column": 0,
                "item": tuple(tree.children),
                "line": 0,
            }
        )
