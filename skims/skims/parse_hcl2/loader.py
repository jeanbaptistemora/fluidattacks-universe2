# Standard library
import ast
from typing import (
    Any,
    List,
)

# Third party libraries
from hcl2.transformer import (
    DictTransformer,
)
from hcl2.lark_parser import (
    DATA,
    Lark_StandAlone,
)
import lark

# Local libraries
from parse_hcl2.tokens import (
    Attribute,
)

# Side effects
DATA['options']['propagate_positions'] = True


class HCL2Builder(  # pylint: disable=too-few-public-methods
    lark.Transformer,  # type: ignore
):

    def __init__(self) -> None:
        self.transformer = DictTransformer()
        super().__init__()

    def new_line_and_or_comma(self, args: List[Any]) -> lark.Discard:
        return self.transformer.new_line_and_or_comma(args)

    def new_line_or_comment(self, args: List[Any]) -> lark.Discard:
        return self.transformer.new_line_or_comment(args)


def load(stream: str) -> Any:
    return post_process(Lark_StandAlone(HCL2Builder()).parse(stream))


def post_process(data: Any) -> Any:
    data = remove_discarded(data)
    data = coerce_to_string_lit(data)
    data = coerce_to_boolean(data)
    data = replace_attributes(data)

    return data


def remove_discarded(data: Any) -> Any:
    if isinstance(data, lark.Tree):
        data.children = [
            post_process(children)
            for children in data.children
            if not isinstance(children, lark.Discard)
        ]

    return data


def coerce_to_boolean(data: Any) -> Any:
    if isinstance(data, lark.Tree):
        if data.data == 'true_lit' and not data.children:
            data = True
        elif data.data == 'false_lit' and not data.children:
            data = False
        else:
            data.children = list(map(coerce_to_string_lit, data.children))

    return data


def coerce_to_string_lit(data: Any) -> Any:
    if isinstance(data, lark.Tree):
        data.children = list(map(coerce_to_string_lit, data.children))
    elif isinstance(data, lark.Token):
        if data.type == '__ANON_3':
            data = data.value
        elif data.type == 'STRING_LIT':
            data = ast.literal_eval(data.value)

    return data


def replace_attributes(data: Any) -> Any:
    if isinstance(data, lark.Tree):
        if data.data == 'attribute' and data.children[0].data == 'identifier':
            data = Attribute(
                key=data.children[0].children[0],
                val=data.children[1],
            )
        else:
            data.children = list(map(replace_attributes, data.children))

    return data
