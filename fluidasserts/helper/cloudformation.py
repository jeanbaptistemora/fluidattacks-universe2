"""AWS CloudFormation helper."""

# standard imports
import json
import contextlib
from typing import Any, Dict, Iterator, Tuple

# 3rd party imports
import yaml
import magic

# Constants
Template = Dict[str, Any]
ResourceName = str
ResourceProperties = Dict[str, Any]


class CloudFormationError(Exception):
    """Base class for all errors in this module."""


class UnrecognizedTemplateFormat(CloudFormationError):
    """The template is not JSON or YAML compliant."""


class UnrecognizedType(CloudFormationError):
    """The Value is not of recognized type."""

#
# Type casters
#


def to_boolean(obj: str) -> bool:
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
    magic_obj = magic.Magic(mime_encoding=True)
    with open(template_path) as raw_file_handle:
        encoding = magic_obj.from_buffer(raw_file_handle.read())

    with open(template_path, encoding=encoding) as template_handle:
        template_contents: str = template_handle.read()

    with contextlib.suppress(yaml.scanner.ScannerError):
        return yaml.safe_load(template_contents)

    with contextlib.suppress(json.JSONDecodeError):
        return json.loads(template_contents)

    raise CloudFormationError('Template is not JSON or YAML')


def iterate_resources_in_template(
        template_path: str,
        *resource_types: str) -> Iterator[
            Tuple[ResourceName, ResourceProperties]]:
    """Yield resources of the provided types."""
    template: Template = load_template(template_path)
    for res_name, res_data in template.get('Resources', {}).items():
        res_type = res_data['Type']
        if res_type in resource_types:
            yield res_name, res_data.get('Properties')
