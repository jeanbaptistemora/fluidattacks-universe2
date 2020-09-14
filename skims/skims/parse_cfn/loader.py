# Standard library
from typing import (
    Any,
)

# Third party libraries
from cfn_tools.yaml_loader import (
    CfnYamlLoader,
    construct_mapping,
    multi_constructor,
    TAG_MAP,
)
import yaml


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


Loader.add_constructor(TAG_MAP, overloaded_construct_mapping)
Loader.add_multi_constructor("!", overloaded_multi_constructor)
