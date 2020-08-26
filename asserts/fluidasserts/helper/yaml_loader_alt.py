"""
Yaml Loader Custom.

Custom YAML loader with added line number information for CloudFormation.
"""

from cfn_tools import yaml_loader

# pylint: disable=too-many-ancestors


class LineLoader(yaml_loader.CfnYamlLoader):
    """Custom YAML Loader class for CFN templates."""


def construct_mapping(self, node, deep=False):
    """Add line number to CFN resources."""
    mapping = yaml_loader.construct_mapping(self, node, deep=deep)
    mapping['__line__'] = node.start_mark.line
    return mapping


LineLoader.add_constructor(yaml_loader.TAG_MAP, construct_mapping)
