from lark import (
    Tree,
)
from parse_hcl2.tokens import (
    Attribute,
    Block,
)
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    Union,
)


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
    *expected_kinds: str,
) -> Iterator[Block]:
    if isinstance(model, Tree):
        for child in model.children:
            yield from iterate_resources(
                child,
                expected_source,
                *expected_kinds,
            )
    elif isinstance(model, Block) and (
        len(model.namespace) == 3
        and model.namespace[0] == expected_source
        and model.namespace[1] in expected_kinds
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
    body: List[Union[Attribute, Block]], key: str, default: Any = None
) -> Union[Any, Block]:
    for item in body:
        if isinstance(item, Block):
            continue
        if isinstance(item, Attribute) and item.key == key:
            return item
    return default
