"""AWS CloudFormation helper."""

# standard imports
from typing import Any, Dict, Iterator, Tuple

# 3rd party imports
import yaml
import cfn_tools

# local imports
from fluidasserts.utils.generic import get_paths

# Constants
Template = Dict[str, Any]
ResourceName = str
ResourceProperties = Dict[str, Any]

#
# Exceptions
#


class CloudFormationError(Exception):
    """Base class for all errors in this module."""


class UnrecognizedTemplateFormat(CloudFormationError):
    """The template is not JSON or YAML compliant."""


class UnrecognizedType(CloudFormationError):
    """The Value is not of recognized type."""

#
# Type casters
#


def to_boolean(obj: str, default: bool) -> bool:
    """True if obj is a CloudFormation boolean, False otherwise."""
    if obj in (True, 'true', 'True', '1', 1):
        return True
    if obj in (False, 'false', 'False', '0', 0):
        return False
    raise UnrecognizedType(f'{obj} is not a CloudFormation boolean')


#
# Helpers
#

def load_template(template_path: str) -> Template:
    """Return the CloudFormation content of the template on `template_path`."""
    try:
        with open(template_path,
                  encoding='utf-8',
                  errors='replace') as template_handle:
            template_contents: str = template_handle.read()

        contents = cfn_tools.load_yaml(template_contents)

        if not isinstance(contents, cfn_tools.odict.ODict):
            raise UnrecognizedTemplateFormat('Not a CloudFormation template')

    except (yaml.parser.ParserError,
            yaml.scanner.ScannerError,
            yaml.composer.ComposerError,
            UnrecognizedTemplateFormat) as exc:
        raise CloudFormationError(f'Type {type(exc)}, {exc}')
    return contents


def iterate_resources_in_template(
        starting_path: str,
        resource_types: list,
        exclude: list = None,
        ignore_errors: bool = True) -> Iterator[
            Tuple[ResourceName, ResourceProperties]]:
    """Yield resources of the provided types."""
    exclude = tuple(exclude or [])
    for template_path in get_paths(
            starting_path, exclude=exclude, endswith=('.yml', '.yaml')):
        try:
            template: Template = load_template(template_path)
            for res_name, res_data in template.get('Resources', {}).items():
                if res_name.startswith('Fn::') \
                        or res_name.startswith('!') \
                        or res_data['Type'] not in resource_types:
                    continue

                yield template_path, res_name, res_data.get('Properties')
        except CloudFormationError as exc:
            if not ignore_errors:
                raise exc
