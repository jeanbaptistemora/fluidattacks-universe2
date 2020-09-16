# Standard library
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from cfn_tools.yaml_loader import (
    CfnYamlLoader,
    construct_mapping,
    multi_constructor,
    TAG_MAP,
)
from frozendict import (
    frozendict,
)
import yaml

# Local libraries
from parse_json import (
    blocking_loads,
)


class Loader(  # pylint: disable=too-many-ancestors
    CfnYamlLoader,  # type: ignore
):
    pass


def overloaded_construct_mapping(
    self: yaml.Loader,
    node: yaml.Node,
    deep: bool = False,
) -> Any:
    mapping = dict(construct_mapping(self, node, deep=deep))
    mapping['__column__'] = node.start_mark.column
    mapping['__line__'] = node.start_mark.line
    return mapping


def overloaded_multi_constructor(
    loader: yaml.Loader,
    tag_suffix: str,
    node: yaml.Node,
) -> Any:
    mapping = dict(multi_constructor(loader, tag_suffix, node))
    mapping['__column__'] = node.start_mark.column
    mapping['__line__'] = node.start_mark.line
    return mapping


def load_as_yaml_without_line_number(content: str) -> Any:
    return load_as_yaml(content, loader_cls=CfnYamlLoader)


def load_as_yaml(content: str, *, loader_cls=Loader) -> Any:
    loader = loader_cls(content)
    try:
        return loader.get_single_data()
    finally:
        loader.dispose()


def load_as_json(content: str) -> Any:

    def _is_meta(node: Any) -> bool:
        if isinstance(node, frozendict):
            return set(node) == {'column', 'item', 'line'}
        return False

    # We cannot get the line number of compound objects as yaml does
    # so let's assume the line number of the compound object if the first one
    # saw
    def _create_obj(
        last_c: int,
        last_l: int,
        obj: Any,
    ) -> Any:
        if isinstance(obj, frozendict):
            obj_copy = {}
            for key, value in obj.items():
                if _is_meta(value):
                    last_c, last_l = value['column'], value['line']
                    value = value['item']
                if _is_meta(key):
                    last_c, last_l = key['column'], key['line']
                    key = key['item']

                obj_copy.setdefault('__column__', last_c)
                obj_copy.setdefault('__line__', last_l)

                obj_copy[_create_obj(
                    last_c=last_c,
                    last_l=last_l,
                    obj=key,
                )] = _create_obj(
                    last_c=last_c,
                    last_l=last_l,
                    obj=value,
                )
        elif isinstance(obj, tuple):
            obj_copy = [
                _create_obj(
                    last_c=last_c,
                    last_l=last_l,
                    obj=value['item'] if _is_meta(value) else value,
                )
                for value in obj
            ]
        else:
            obj_copy = obj

        return obj_copy

    return _create_obj(
        last_c=0,
        last_l=1,
        obj=blocking_loads(content, default={}),
    )


async def load(content: str, fmt: str) -> Any:
    if fmt in {'yml', 'yaml'}:
        return await in_process(load_as_yaml, content)

    if fmt in {'json'}:
        return await in_process(load_as_json, content)

    return {}


Loader.add_constructor(TAG_MAP, overloaded_construct_mapping)
Loader.add_multi_constructor("!", overloaded_multi_constructor)
