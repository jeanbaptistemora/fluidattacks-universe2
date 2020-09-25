# Standard library
from typing import (
    Any, )

# Third party libraries
from cfn_tools.yaml_loader import (
    construct_mapping,
    multi_constructor,
    TAG_MAP,
)
import yaml

# Local libraries
from parse_common.types import (
    DictToken,
    FloatToken,
    IntToken,
    ListToken,
    StringToken,
)


class BasicLoader(  # pylint: disable=too-many-ancestors
        yaml.SafeLoader, ):
    pass


class Loader(  # pylint: disable=too-many-ancestors
        yaml.SafeLoader, ):
    pass


def overloaded_multi_constructor(
    loader: yaml.Loader,
    tag_suffix: str,
    node: yaml.Node,
) -> Any:
    if isinstance(node.value, str):
        node.value = StringToken(
            value=node.value,
            column=node.start_mark.column + 1,
            line=node.start_mark.line + 1,
        )
    return DictToken(
        value=multi_constructor(loader, tag_suffix, node),
        column=node.start_mark.column + 1,
        line=node.start_mark.line + 1,
    )


def overloaded_construct_yaml_timestamp(
    self: yaml.Loader,
    node: yaml.Node,
) -> str:
    return self.construct_yaml_timestamp(node).isoformat()


def load_as_yaml_without_line_number(content: str) -> Any:
    return loads(content, loader_cls=BasicLoader)


def overloaded_construct_mapping(
    self: yaml.Loader,
    node: yaml.Node,
    deep: bool = False,
) -> DictToken:
    return DictToken(
        value=construct_mapping(self, node, deep=deep),
        column=node.start_mark.column + 1,
        line=node.start_mark.line + 1,
    )


def overloaded_construct_sequence(
    self: yaml.Loader,
    node: yaml.Node,
    deep: bool = False,
) -> ListToken:
    return ListToken(
        value=[
            self.construct_object(child, deep=deep) for child in node.value
        ],
        column=node.start_mark.column + 1,
        line=node.start_mark.line + 1,
    )


def overloaded_construct_float(
    _: yaml.Loader,
    node: yaml.Node,
    __: bool = False,
) -> FloatToken:
    return FloatToken(
        value=node.value,
        column=node.start_mark.column + 1,
        line=node.start_mark.line + 1,
    )


def overloaded_construct_int(
    _: yaml.Loader,
    node: yaml.Node,
    __: bool = False,
) -> IntToken:
    return IntToken(
        value=node.value,
        column=node.start_mark.column + 1,
        line=node.start_mark.line + 1,
    )


def overloaded_construct_str(
    _: yaml.Loader,
    node: yaml.Node,
    __: bool = False,
) -> StringToken:
    return StringToken(
        value=node.value,
        column=node.start_mark.column + 1,
        line=node.start_mark.line + 1,
    )


def loads(content: str, *, loader_cls=Loader) -> Any:  # type: ignore
    try:
        loader = loader_cls(content)
        try:
            if loader.check_data():
                return loader.get_data()
            return {}
        finally:
            loader.dispose()
    except yaml.error.YAMLError:
        return {}


# override a Basic loader
BasicLoader.add_constructor(
    'tag:yaml.org,2002:timestamp',
    overloaded_construct_yaml_timestamp,
)
BasicLoader.add_constructor(TAG_MAP, construct_mapping)
BasicLoader.add_multi_constructor("!", multi_constructor)

# override
# override datetimes
Loader.add_constructor(
    'tag:yaml.org,2002:timestamp',
    overloaded_construct_yaml_timestamp,
)

# override maps
Loader.add_constructor(TAG_MAP, overloaded_construct_mapping)
# override lists o seq
Loader.add_constructor('tag:yaml.org,2002:seq', overloaded_construct_sequence)
# override float
Loader.add_constructor('tag:yaml.org,2002:float', overloaded_construct_float)
# override int
Loader.add_constructor('tag:yaml.org,2002:int', overloaded_construct_int)
# override str
Loader.add_constructor('tag:yaml.org,2002:str', overloaded_construct_str)
# override !
Loader.add_multi_constructor("!", overloaded_multi_constructor)
