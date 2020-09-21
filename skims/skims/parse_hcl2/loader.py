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
    Block,
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


def load(stream: str, *, default: Any = None) -> Any:
    try:
        return post_process(Lark_StandAlone(HCL2Builder()).parse(stream))
    except lark.exceptions.LarkError:
        if default:
            return default
        raise


def post_process(data: Any) -> Any:
    data = remove_discarded(data)
    data = coerce_to_int_lit(data)
    data = coerce_to_string_lit(data)
    data = coerce_to_boolean(data)
    data = extract_single_expr_term(data)
    data = load_objects(data)
    data = replace_attributes(data)
    data = load_blocks(data)

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


def coerce_to_int_lit(data: Any) -> Any:
    if isinstance(data, lark.Tree):
        if data.data == 'int_lit':
            data = int(''.join(child.value for child in data.children))
        else:
            data.children = list(map(coerce_to_int_lit, data.children))
    elif isinstance(data, lark.Token):
        if data.type == '__ANON_3':
            data = data.value
        elif data.type == 'STRING_LIT':
            data = ast.literal_eval(data.value)

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


def extract_single_expr_term(data: Any) -> Any:
    if isinstance(data, lark.Tree):
        if data.data == 'expr_term' and len(data.children) == 1:
            data = extract_single_expr_term(data.children[0])
        else:
            data.children = list(map(extract_single_expr_term, data.children))
    return data


def load_blocks(data: Any) -> Any:
    if isinstance(data, lark.Tree):
        if data.data == 'block':
            body = []
            namespace = []
            for child in data.children:
                if isinstance(child, lark.Tree) and child.data == 'body':
                    body = list(map(load_blocks, child.children))
                elif isinstance(child, lark.Tree) \
                        and child.data == 'identifier':
                    namespace.append(child.children[0])
                else:
                    namespace.append(child)

            data = Block(
                body=body,
                column=data.column - 1,
                line=data.line,
                namespace=namespace,
            )
        else:
            data.children = list(map(load_blocks, data.children))
    return data


def load_objects(data: Any) -> Any:
    if isinstance(data, lark.Tree) and data.data == 'object':
        if all(
            children.data == 'object_elem'
            and children.children[0].data == 'identifier'
            for children in data.children
        ):
            copy = {
                children.children[0].children[0]: children.children[1]
                for children in data.children
            }
            data = copy
        else:
            data.children = list(map(extract_single_expr_term, data.children))
    return data


def replace_attributes(data: Any) -> Any:
    if isinstance(data, lark.Tree):
        if data.data == 'attribute' and data.children[0].data == 'identifier':
            data = Attribute(
                column=data.column - 1,
                key=data.children[0].children[0],
                line=data.line,
                val=data.children[1],
            )
        else:
            data.children = list(map(replace_attributes, data.children))

    return data
