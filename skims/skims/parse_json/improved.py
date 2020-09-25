# Standard library
import ast
from typing import (
    Any,
    Optional,
    Union,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from frozendict import (
    frozendict
)
import lark

# Local library
from parse_common.types import (
    DictToken,
    FloatToken,
    IntToken,
    ListToken,
    StringToken,
    TupleToken
)

# Constants
GRAMMAR = r"""
    ?start: value

    ?value: object
            | array
            | string
            | SIGNED_NUMBER      -> number
            | single

    array  : init_array [value ("," value)*] end_array
    object : init_object [pair ("," pair)*] end_object
    pair   : string ":" value

    false : "false"
    true : "true"
    null : "null"
    single : false | true | null
    string : ESCAPED_STRING
    init_object: "{"
    end_object: "}"
    init_array: "["
    end_array: "]"

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
) -> Any:
    return await in_process(blocking_loads, stream, default=default)


class JSONBuilder(
    lark.Transformer,  # type: ignore
):

    single_map = {
        "false": False,
        "null": None,
        "true": True,
    }

    @staticmethod
    @lark.v_args(tree=True)  # type: ignore
    def single(tree: lark.Tree) -> Union[bool, None]:
        children: lark.Tree = tree.children[0]
        return JSONBuilder.single_map[children.data]

    @staticmethod
    @lark.v_args(inline=True)  # type: ignore
    def string(token: lark.Token) -> StringToken:
        return StringToken(
            value=ast.literal_eval(token),
            line=token.line,
            column=token.column,
        )

    @staticmethod
    @lark.v_args(inline=True)  # type: ignore
    def number(token: lark.Token) -> Union[FloatToken, IntToken]:
        value = ast.literal_eval(token)
        if isinstance(value, float):
            return FloatToken(
                column=token.column,
                line=token.line,
                value=value,
            )
        return IntToken(
            column=token.column,
            line=token.line,
            value=value,
        )

    @staticmethod
    @lark.v_args(tree=True)  # type: ignore
    def array(tree: lark.Tree) -> ListToken:
        init = tree.children.pop(0)
        tree.children.pop(-1)
        return ListToken(
            column=init.column,
            value=tree.children,
            line=init.line,
        )

    @staticmethod
    @lark.v_args(inline=True)  # type: ignore
    def pair(one: StringToken, two: Any) -> TupleToken:
        return TupleToken(
            column=one.__column__,
            value=(
                one,
                two,
            ),
            line=one.__line__,
        )

    @staticmethod
    @lark.v_args(tree=True)  # type: ignore
    def object(tree: lark.Tree) -> DictToken:
        init = tree.children.pop(0)
        tree.children.pop(-1)
        return DictToken(
            value={key: value
                   for (  # pylint: disable=unnecessary-comprehension
                       key,
                       value,
                   ) in tree.children},
            line=init.line,
            column=init.column,
        )
