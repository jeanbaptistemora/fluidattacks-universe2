# -*- coding: utf-8 -*-

"""
Fluid Asserts main package.

Functions trim, reindent and parse_docstring taken from openstack/rally
but were slightly modified to fit this project.
"""

# standard imports
import importlib
import os
import re
import sys
import json
import types
import inspect
import textwrap
import collections
from datetime import datetime
from typing import Callable, Dict, OrderedDict, List, Any

# 3rd party imports
from pkg_resources import get_distribution, DistributionNotFound
import oyaml as yaml
from yaml.dumper import SafeDumper
from yaml.representer import SafeRepresenter as SafeRepres

# local imports
from fluidasserts.utils import constants

# Objects that are not standard YAML Nodes will be represented as follows:
#   Ordered dictionaries
yaml.add_multi_representer(
    collections.OrderedDict, lambda _, x: SafeRepres().represent_dict(
        x), SafeDumper)
#   Function objects -> function( args in definition ... )
yaml.add_multi_representer(
    types.FunctionType, lambda _, x: SafeRepres().represent_str(
        f'function{inspect.signature(x)}'), SafeDumper)
#   Objects -> type(object)
yaml.add_multi_representer(
    object, lambda _, x: SafeRepres().represent_str(
        str(type(x))), SafeDumper)

# Constants
OPEN: str = 'OPEN'
CLOSED: str = 'CLOSED'
UNKNOWN: str = 'UNKNOWN'
ERROR: str = 'ERROR'

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
    desc = docstring['short_description']
    desc = re.sub(r'`_.', '', desc)
    desc = re.sub(r'[`<>\\]', '', desc)
    return desc


# Do not handle this vars directly, use the methods
METHOD_STATS = {}
METHOD_STATS_OWNER = 'global'


def method_stats_set_owner(owner: str) -> bool:
    """Set the current owner of METHOD_STATS."""
    # pylint: disable=global-statement
    global METHOD_STATS, METHOD_STATS_OWNER
    METHOD_STATS_OWNER = owner.replace(':', '')

    if METHOD_STATS_OWNER not in METHOD_STATS:
        METHOD_STATS[METHOD_STATS_OWNER] = {}
    return True


def method_stats_parse_stats() -> dict:
    """Return a nice looking METHOD_STATS."""
    method_stats = [
        {
            owner: {
                method: (
                    f'{res[OPEN]} open, '
                    f'{res[CLOSED]} closed, '
                    f'{res[UNKNOWN]} unknown')
                for method, res in methods.items()
            }
        }
        for owner, methods in METHOD_STATS.items()
    ]
    return method_stats


class Unit():
    """API class for a testing unit."""

    def __init__(self,
                 *,
                 where: str,
                 source: str = None,
                 specific: List[Any],
                 fingerprint: str = None):
        """Default constructor."""
        self.where: str = where
        self.source: str = source
        self.specific: List[Any] = specific
        self.fingerprint: str = fingerprint

    def total_incidences(self) -> int:
        """Return the number of incidences in this unit."""
        return len(self.specific)

    def as_dict(self) -> dict:
        """Dict representation of this class."""
        result: OrderedDict[str, Any] = collections.OrderedDict()

        result['where'] = self.where

        if constants.VERBOSE_CHECKS and self.source:
            result['source'] = self.source

        if self.specific:
            # Stringify
            specific = map(str, self.specific)
            # Escape commas:
            specific = map(lambda x: x.replace('\\', '\\\\'), specific)
            specific = map(lambda x: x.replace(',', '\\,'), specific)
            # Join to make it less verbose
            specific = ', '.join(specific)

            result['specific'] = specific

        if constants.VERBOSE_CHECKS and self.fingerprint:
            result['fingerprint'] = self.fingerprint

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

        self.status: str = None
        self.message: str = None
        self.duration: float = None
        self.safes: List[Unit] = None
        self.vulns: List[Unit] = None

        _func: Callable = func
        # Adding decorators to a function modify its metadata, fortunately
        # The wrapper function will keep a reference to the wrapped function
        #   (if you use functools.update_wrapper)
        # In order to extract the original metadata let's climb the stack
        #   (see functools.update_wrapper's source code)
        while hasattr(_func, '__wrapped__'):
            _func = getattr(_func, '__wrapped__')

        # This will set self.func_params to a dict with the args used at call:
        #   example:
        #     f = lambda a, *b, c=None, **d:
        #   called with:
        #     f(1, 2, 3, g=3, c=5)
        #   self.func_params:
        #     {'a': 1, 'b': (2, 3), 'c': 5, 'd': {'g': 3}}
        func_sig: inspect.Signature = inspect.signature(_func)
        func_bind: inspect.BoundArguments = \
            func_sig.bind(*func_args, **func_kwargs)
        func_bind.apply_defaults()
        self.func_params = func_bind.arguments

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

    def get_vulns_number(self) -> int:
        """Return the number of incidences of all vulnerabilities."""
        if hasattr(self, 'vulns'):
            return sum(v.total_incidences() for v in self.vulns)
        return 0

    def get_safes_number(self) -> int:
        """Return the number of incidences of all safe units."""
        if hasattr(self, 'safes'):
            return sum(s.total_incidences() for s in self.safes)
        return 0

    def register_stats(self) -> bool:
        """Register this result stats."""
        # pylint: disable=global-statement
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
        result: OrderedDict[str, Any] = collections.OrderedDict()
        result['check'] = self.func_id
        result['description'] = self.func_desc
        result['status'] = self.status
        if constants.VERBOSE_CHECKS:
            result['message'] = self.message
        if self.vulns:
            result['vulnerabilities'] = [v.as_dict() for v in self.vulns]
        if constants.VERBOSE_CHECKS and self.safes and len(self.safes) <= 10:
            result['secure-units'] = [v.as_dict() for v in self.safes]
        if constants.VERBOSE_CHECKS and self.func_params:
            result['parameters'] = self.func_params
        if constants.VERBOSE_CHECKS:
            result['vulnerable_incidences'] = self.get_vulns_number()
            result['when'] = self.when
        if constants.VERBOSE_CHECKS and hasattr(self, 'duration'):
            result['elapsed_seconds'] = self.duration
        result['test_kind'] = self.kind
        result['risk'] = self.risk
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
        if self.is_closed():
            return False
        if self.is_unknown():
            return False
        raise ValueError(
            f'status is set to an unsupported value: {self.status}')

    def __str__(self):
        """Cast to string."""
        return json.dumps(self.as_dict(), indent=4)


def _get_result_as_tuple_sast(*,
                              path: str,
                              msg_open: str, msg_closed: str,
                              open_if: bool,
                              fingerprint: Any = None) -> tuple:
    """Return the tuple version of the Result object."""
    unit: Unit = Unit(where=path,
                      specific=[msg_open if open_if else msg_closed],
                      fingerprint=fingerprint)

    if open_if:
        return OPEN, msg_open, [unit], []
    return CLOSED, msg_closed, [], [unit]


def _get_result_as_tuple_host_port(*,
                                   protocol: str, host: str, port: int,
                                   msg_open: str, msg_closed: str,
                                   open_if: bool,
                                   auth: tuple = None,
                                   extra: str = None,
                                   fingerprint: Any = None) -> tuple:
    """Return the tuple version of the Result object."""
    auth_str: str = (
        (f'{auth[0]}' if auth and auth[0] else str()) +
        (f':{auth[1]}' if auth and auth[1] else str()))

    where: str = (
        f'{protocol}://{auth_str}' +
        ('@' if auth_str else str()) +
        f'{host}:{port}' +
        f'/{extra}' if extra else str())

    unit: Unit = Unit(where=where,
                      specific=[msg_open if open_if else msg_closed],
                      fingerprint=fingerprint)

    if open_if:
        return OPEN, msg_open, [unit], []
    return CLOSED, msg_closed, [], [unit]


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
else:
    __version__ = _DIST.version
