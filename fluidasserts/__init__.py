# -*- coding: utf-8 -*-

"""
Fluid Asserts main package.

Functions trim, reindent and parse_docstring taken from openstack/rally
but were slightly modified to fit this project.
"""

# standard imports
from __future__ import absolute_import

import importlib
import inspect
import os
import re
import sys
import json
import textwrap
from datetime import datetime
from typing import Callable, Dict, List, Any

# 3rd party imports
from pkg_resources import get_distribution, DistributionNotFound
import oyaml as yaml

# local imports
# none


# Constants
OPEN: str = 'OPEN'
CLOSED: str = 'CLOSED'
UNKNOWN: str = 'UNKNOWN'

LOW: str = 'low'
MEDIUM: str = 'medium'
HIGH: str = 'high'

SAST: str = 'SAST'
DAST: str = 'DAST'

PARAM_OR_RETURNS_REGEX = re.compile(r":(?:param|returns)")
RETURNS_REGEX = re.compile(r":returns: (?P<doc>.*)", re.S)
PARAM_REGEX = re.compile(r":param (?P<name>[\*\w]+): (?P<doc>.*?)"
                         r"(?:(?=:param)|(?=:return)|(?=:raises)|\Z)", re.S)

LOCAL_TZ = datetime.utcnow().astimezone().tzinfo
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods


def check_cli():
    """Check execution from CLI."""
    if 'FA_CLI' not in os.environ:
        cli_warn = textwrap.dedent("""
            ########################################################
            ## INVALID OUTPUT. PLEASE, RUN ASSERTS USING THE CLI. ##
            ########################################################
            """)
        print(cli_warn)


def trim(docstring):
    """Trim function from PEP-257."""
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
    desc = re.sub(r'`_.', '', desc)
    desc = re.sub(r'[`<>\\]', '', desc)
    return desc


def get_caller_module(depth: int = 3) -> str:
    """Get caller module."""
    frm = inspect.stack()[depth]
    mod = inspect.getmodule(frm[0])
    return mod.__name__


def get_caller_function(depth: int = 3) -> str:
    """Get caller function."""
    function = sys._getframe(depth).f_code.co_name  # noqa
    while function.startswith('_'):
        function = sys._getframe(depth).f_code.co_name  # noqa
        depth += 1
    return function


# Do not handle this vars directly, use the methods
METHOD_STATS = {}
METHOD_STATS_OWNER = 'global'


def method_stats_set_owner(owner: str) -> bool:
    """Set the current owner of METHOD_STATS."""
    global METHOD_STATS_OWNER
    METHOD_STATS_OWNER = owner.replace(':', '')
    return True


def method_stats_register_caller(with_status: str) -> bool:
    """Register the current finding and Asserts module in METHOD_STATS."""
    caller_module: str = get_caller_module()
    caller_function: str = get_caller_function()
    caller: str = f"{caller_module}.{caller_function}"
    caller = re.sub(r'^fluidasserts\.', '', caller)
    if METHOD_STATS_OWNER not in METHOD_STATS:
        METHOD_STATS[METHOD_STATS_OWNER] = {}
    try:
        METHOD_STATS[METHOD_STATS_OWNER][caller][with_status] += 1
    except KeyError:
        METHOD_STATS[METHOD_STATS_OWNER][caller] = {
            OPEN: 0, CLOSED: 0, UNKNOWN: 0}
        METHOD_STATS[METHOD_STATS_OWNER][caller][with_status] += 1
    return True


def method_stats_parse_stats() -> dict:
    """Return a nice looking METHOD_STATS."""
    method_stats = {
        owner: {
            method: "{} open, {} closed, {} unknown".format(
                res[OPEN], res[CLOSED], res[UNKNOWN])
            for method, res in methods.items()
        }
        for owner, methods in METHOD_STATS.items()
    }
    return method_stats


class Message():
    """Output message class."""

    def __init__(
            self,
            status: str,
            message: str,
            details: dict) -> None:
        """Create constructor method."""
        self.__status_codes = [OPEN, CLOSED, UNKNOWN]
        self.date = datetime.now()
        self.status: str = status
        self.message: str = message
        self.details: dict = details if isinstance(details, dict) else {}
        self.caller_module: str = get_caller_module()
        self.caller_function: str = get_caller_function()
        self.check: str = f'{self.caller_module}.{self.caller_function}'
        self.module_description = get_module_description(self.caller_module,
                                                         self.caller_function)

    def __build_message(self):
        """Build message dict."""
        data = {}
        data['check'] = self.check
        if 'metadata' not in self.details:
            data['description'] = self.module_description
        data['status'] = self.status
        data['message'] = self.message
        if self.details:
            data['details'] = self.details
        data['when'] = self.date
        return data

    def as_yaml(self):
        """Get YAML representation of message."""
        return yaml.safe_dump(self.__build_message(),
                              default_flow_style=False,
                              explicit_start=True,
                              allow_unicode=True)


class Unit():
    """API class for a testing unit."""

    def __init__(self,
                 *,
                 where: str,
                 source: str,
                 specific: List[Any],
                 fingerprint: str = None):
        """Default constructor."""
        self.where: str = where
        self.source: str = source
        self.specific: List[Any] = specific
        self.fingerprint: str = fingerprint

    def as_dict(self) -> dict:
        """Dict reprensentation of this class."""
        result: Dict[str, Any] = {}

        result.update({'where': self.where})
        result.update({'source': self.source})

        # Stringify
        specific = self.specific if self.specific else [None]
        specific = map(str, specific)
        # Escape commas:
        specific = map(lambda x: x.replace(r'\\', r'\\\\'), specific)
        specific = map(lambda x: x.replace(r',', r'\\,'), specific)
        # Join to make it less verbose
        specific = ', '.join(specific)

        result.update({'specific': specific})
        result.update({'fingerprint': self.fingerprint})
        return result


class Result():
    """API response class."""

    def __init__(self,
                 risk: str,
                 kind: str,
                 func: Callable,
                 func_args: List[Any],
                 func_kwargs: Dict[str, Any]):
        """Default constructor."""
        self.risk: str = risk
        self.kind: str = kind
        self.when: str = datetime.now(tz=LOCAL_TZ).strftime(DATE_FORMAT)
        self.func_id: str = func.__module__ + ' -> ' + func.__name__
        self.func_desc: str = get_module_description(func.__module__,
                                                     func.__name__)

        func_params: Dict[str, Any] = {}

        func_vars = func.__code__.co_varnames
        func_nargs = len(func_args)
        func_nkwargs = len(func_vars) - func_nargs

        # Append the args and the kwargs
        func_params.update({func_vars[i]: func_args[i]
                            for i in range(func_nargs)})
        func_params.update({func_vars[i]: func_kwargs.get(func_vars[i])
                            for i in range(func_nargs, func_nkwargs)})

        # Filter not supplied values
        self.func_params: Dict[str, Any] = \
            {k: v for k, v in func_params.items() if v is not None}

    def set_status(self, status: str) -> bool:
        """Set the status."""
        self.status: str = status
        return True

    def set_duration(self, duration: int) -> bool:
        """Set the duration."""
        self.duration: int = duration
        return True

    def set_message(self, message: str) -> bool:
        """Set the message."""
        self.message: str = message
        return True

    def set_vulns(self, vulns: List[Unit]) -> bool:
        """Set the vulns."""
        self.vulns: List[Unit] = vulns
        return True

    def set_safes(self, safes: List[Unit]) -> bool:
        """Set the safes."""
        self.safes: List[Unit] = safes
        return True

    def register_stats(self) -> bool:
        """Register this result stats."""
        global METHOD_STATS, METHOD_STATS_OWNER
        if METHOD_STATS_OWNER not in METHOD_STATS:
            METHOD_STATS[METHOD_STATS_OWNER] = {}
        try:
            METHOD_STATS[METHOD_STATS_OWNER][self.func_id][self.status] += 1
        except KeyError:
            METHOD_STATS[METHOD_STATS_OWNER][self.func_id] = {
                OPEN: 0, CLOSED: 0, UNKNOWN: 0}
            METHOD_STATS[METHOD_STATS_OWNER][self.func_id][self.status] += 1
        return True

    def as_dict(self) -> dict:
        """Return a dict representation of the class."""
        result = {}
        result.update({
            'check': self.func_id,
            'description': self.func_desc,
            'status': self.status,
            'message': self.message,
        })
        if self.vulns:
            result['vulnerabilities'] = [v.as_dict() for v in self.vulns]
        if self.safes and len(self.safes) <= 10:
            result['secure-units'] = [v.as_dict() for v in self.safes]
        result.update({
            'parameters': self.func_params,
            'when': self.when,
            'elapsed_seconds': self.duration,
            'test_kind': self.kind,
            'risk': self.risk,
        })
        return result

    def print(self) -> bool:
        """Print to stdout the results."""
        kwargs: Dict[str, bool] = {
            'default_flow_style': False,
            'explicit_start': True,
            'allow_unicode': True,
        }
        print(yaml.safe_dump(self.as_dict(), **kwargs), end='', flush=True)

    def is_open(self) -> bool:
        """Return True if the Result has OPEN status."""
        return self.status == OPEN

    def is_closed(self) -> bool:
        """Return True if the Result has CLOSED status."""
        return self.status == CLOSED

    def is_unknown(self) -> bool:
        """Return True if the Result has UNKNOWN status."""
        return self.status == UNKNOWN

    def __bool__(self) -> bool:
        """Cast to boolean."""
        if self.is_open():
            return True
        elif self.is_closed():
            return False
        elif self.is_unknown():
            return False
        raise ValueError(
            f'status is set to an unsupported value: {self.status}')

    def __str__(self):
        """Cast to string."""
        return json.dumps(self.as_dict(), indent=4)


def show_close(message, details=None):
    """Show close message."""
    check_cli()
    method_stats_register_caller(CLOSED)
    message = Message(CLOSED, message, details)
    print(message.as_yaml(), end='', flush=True)


def show_open(message, details=None):
    """Show open message."""
    check_cli()
    method_stats_register_caller(OPEN)
    message = Message(OPEN, message, details)
    print(message.as_yaml(), end='', flush=True)


def show_unknown(message, details=None):
    """Show unknown message."""
    check_cli()
    method_stats_register_caller(UNKNOWN)
    message = Message(UNKNOWN, message, details)
    print(message.as_yaml(), end='', flush=True)


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
