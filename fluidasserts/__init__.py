# -*- coding: utf-8 -*-

"""
Fluid Asserts main package.

Functions trim, reindent and parse_docstring taken from openstack/rally
but were slightly modified to fit this project.
"""

# standard imports
from __future__ import absolute_import

import datetime
import importlib
import inspect
import os
import re
import sys
from collections import OrderedDict

# 3rd party imports
from pkg_resources import get_distribution, DistributionNotFound
import oyaml as yaml


# local imports
# none

PARAM_OR_RETURNS_REGEX = re.compile(r":(?:param|returns)")
RETURNS_REGEX = re.compile(r":returns: (?P<doc>.*)", re.S)
PARAM_REGEX = re.compile(r":param (?P<name>[\*\w]+): (?P<doc>.*?)"
                         r"(?:(?=:param)|(?=:return)|(?=:raises)|\Z)", re.S)


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods

# Remove support for py2

if sys.version_info < (3,):
    print('Py2 is not longer supported. Please, use a Py3 interpreter to run \
Fluid Asserts')
    sys.exit(-1)


def check_cli():
    """Check execution from CLI."""
    if 'FA_CLI' not in os.environ:
        cli_warn = """
########################################################
## INVALID OUTPUT. PLEASE, RUN ASSERTS USING THE CLI. ##
########################################################
"""
        print(cli_warn)


def trim(docstring):
    """Trim function from PEP-257."""
    if not docstring:
        return ""
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    # Current code/unittests expects a line return at
    # end of multiline docstrings
    # workaround expected behavior from unittests
    if "\n" in docstring:
        trimmed.append("")

    # Return a single string:
    return "\n".join(trimmed)


def reindent(string):
    """Reindent string."""
    return "\n".join(l.strip() for l in string.strip().split("\n"))


def parse_docstring(docstring):
    """Parse the docstring into its components.

    :returns: a dictionary of form
              {
                  "short_description": ...,
                  "long_description": ...,
                  "params": [{"name": ..., "doc": ...}, ...],
                  "returns": ...
              }
    """
    short_description = long_description = returns = ""
    params = []

    if docstring:
        docstring = trim(docstring)

        lines = docstring.split("\n", 1)
        short_description = lines[0]

        if len(lines) > 1:
            long_description = lines[1].strip()

            params_returns_desc = None

            match = PARAM_OR_RETURNS_REGEX.search(long_description)
            if match:
                long_desc_end = match.start()
                params_returns_desc = long_description[long_desc_end:].strip()
                long_description = long_description[:long_desc_end].rstrip()

            if params_returns_desc:
                params = [
                    {"name": name, "doc": trim(doc)}
                    for name, doc in PARAM_REGEX.findall(params_returns_desc)
                ]

                match = RETURNS_REGEX.search(params_returns_desc)
                if match:
                    returns = reindent(match.group("doc"))

    return {
        "short_description": short_description,
        "long_description": long_description,
        "params": params,
        "returns": returns
    }


def get_module_description(package, module):
    """Return the module description based on the docstring."""
    package = importlib.import_module(package)
    mod = getattr(package, module)
    docstring = parse_docstring(mod.__doc__)
    desc = '\n'.join(filter(None, (docstring['short_description'],
                                   docstring['long_description'])))
    return desc


def get_caller_module(depth=3):
    """Get caller module."""
    frm = inspect.stack()[depth]
    mod = inspect.getmodule(frm[0])
    return mod.__name__


def get_caller_function():
    """Get caller function."""
    deep = 3
    function = sys._getframe(deep).f_code.co_name  # noqa
    while function.startswith('_'):
        function = sys._getframe(deep).f_code.co_name  # noqa
        deep += 1
    return function


class Message():
    """Output message class."""

    def __init__(self, status, message, details, references):
        """Constructor method."""
        self.__ref_base = 'https://fluidattacks.com/web/es/defends/'
        self.__status_codes = ['OPEN', 'CLOSED', 'UNKNOWN', 'ERROR']
        self.date = datetime.datetime.now()
        self.status = status
        self.message = message
        self.details = details
        if references:
            self.references = self.__ref_base + references
        else:
            self.references = None
        self.caller_module = get_caller_module()
        self.caller_function = get_caller_function()
        self.check = '{}.{}'.format(self.caller_module, self.caller_function)
        self.module_description = get_module_description(self.caller_module,
                                                         self.caller_function)

    def __build_message(self):
        """Build message dict."""
        if self.details is None:
            details = 'None'
        else:
            import operator
            details = OrderedDict(sorted(self.details.items(),
                                         key=operator.itemgetter(0)))

        data = [('check', self.check),
                ('description', self.module_description),
                ('status', self.status),
                ('message', self.message),
                ('details', details),
                ('when', self.date)]
        if self.references:
            data.append(('references', self.references))
        return OrderedDict(data)

    def as_yaml(self):
        """Get YAML representation of message."""
        return yaml.safe_dump(self.__build_message(), default_flow_style=False,
                              explicit_start=True)


def show_close(message, details=None, refs=None):
    """Show close message."""
    check_cli()
    message = Message('CLOSED', message, details, refs)
    print(message.as_yaml(), end='', flush=True)


def show_open(message, details=None, refs=None):
    """Show open message."""
    check_cli()
    message = Message('OPEN', message, details, refs)
    print(message.as_yaml(), end='', flush=True)


def show_unknown(message, details=None, refs=None):
    """Show unknown message."""
    check_cli()
    message = Message('UNKNOWN', message, details, refs)
    print(message.as_yaml(), end='', flush=True)


def check_boolean_env_var(var_name):
    """Check value of boolean environment variable."""
    if var_name in os.environ:
        accepted_values = ['true', 'false']
        if os.environ[var_name] not in accepted_values:
            print(var_name + ' env variable is \
    set but with an unknown value. It must be "true" or "false".')
            sys.exit(-1)


# Set __version__
try:
    _DIST = get_distribution('fluidasserts')
    # Normalize case for Windows systems
    DIST_LOC = os.path.normcase(_DIST.location)
    HERE = os.path.normcase(__file__)
    if not HERE.startswith(os.path.join(DIST_LOC, 'fluidasserts')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:  # pragma: no cover
    __version__ = _DIST.version

check_boolean_env_var('FA_STRICT')
check_boolean_env_var('FA_NOTRACK')
