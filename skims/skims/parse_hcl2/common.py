from lark import (
    Tree,
)
from parse_hcl2.tokens import (
    Attribute,
    Block,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    TypeVar,
    Union,
)

Tdefault_co = TypeVar("Tdefault_co", covariant=True)


def get_block_attribute(block: Block, key: str) -> Optional[Attribute]:
    for attribute in iterate_block_attributes(block):
        if attribute.key == key:
            return attribute
    return None


def get_block_block(block: Block, namespace: str) -> Optional[Block]:
    for nested_block in iterate_block_blocks(block):
        if nested_block.namespace and nested_block.namespace[0] == namespace:
            return nested_block
    return None


def get_blocks_by_namespace(block: Block, namespace: str) -> Iterator[Block]:
    for nested_block in iterate_block_blocks(block):
        if nested_block.namespace and nested_block.namespace[0] == namespace:
            yield nested_block


def get_attribute_by_block(
    block: Block, namespace: str, key: str
) -> Optional[Attribute]:
    for nested_block in iterate_block_blocks(block):
        if nested_block.namespace and nested_block.namespace[0] == namespace:
            for attribute in iterate_block_attributes(nested_block):
                if attribute.key == key:
                    return attribute
    return None


def iterate_resources(
    model: Any,
    expected_source: str,
    *expected_kinds: Optional[str],
) -> Iterator[Block]:
    if isinstance(model, Tree):
        for child in model.children:
            yield from iterate_resources(
                child,
                expected_source,
                *expected_kinds,
            )
    elif (  # pylint: disable=too-many-boolean-expressions
        isinstance(model, Block) and hasattr(model, "namespace")
    ) and (
        (len(model.namespace) == 1 and model.namespace[0] == expected_source)
        or (
            len(model.namespace) == 3
            and model.namespace[0] == expected_source
            and model.namespace[1] in expected_kinds
        )
    ):
        yield model


def iterate_block_attributes(block: Block) -> Iterator[Attribute]:
    for item in block.body:
        if isinstance(item, Attribute):
            yield item


def iterate_block_blocks(block: Block) -> Iterator[Block]:
    for item in block.body:
        if isinstance(item, Block):
            yield item


def get_argument(
    body: List[Union[Attribute, Block]], key: str, default: Any = None
) -> Union[Any, Block]:
    for item in body:
        if isinstance(item, Attribute):
            continue
        if isinstance(item, Block) and key in item.namespace:
            return item
    return default


def get_attribute(
    body: List[Union[Attribute, Block]],
    key: str,
    default: Optional[Tdefault_co] = None,
) -> Union[Optional[Tdefault_co], Attribute]:
    for item in body:
        if isinstance(item, Block):
            continue
        if isinstance(item, Attribute) and item.key == key:
            return item
    return default


def get_tree_value(tree: Tree) -> Union[str, Dict[str, str]]:
    value_as_str: str = ""
    value_as_dict: Dict[str, str] = {}
    value: Union[str, Dict[str, str]]
    if tree.data == "get_attr_expr_term":
        for idx, child in enumerate(tree.children):
            value = get_tree_value(child)
            if isinstance(value, str):
                if idx == 0:
                    value_as_str = value
                else:
                    value_as_str = ".".join([value_as_str, value])
    if tree.data == "identifier":
        return tree.children[0]
    if tree.data == "object":
        for child in tree.children:
            value = get_tree_value(child)
            if isinstance(value, dict):
                value_as_dict.update(value)
    if tree.data == "object_elem":
        children = tree.children
        return {
            children[0]: (
                str(get_tree_value(children[1]))
                if isinstance(children[1], Tree)
                else children[1]
            )
        }
    return value_as_str or value_as_dict


def get_attribute_value(body: List[Union[Attribute, Block]], key: str) -> Any:
    attr = get_attribute(body, key)
    if isinstance(attr, Attribute):
        value = attr.val
        if isinstance(value, Tree):
            value = get_tree_value(value)
        return value
    return None
