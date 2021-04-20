# Standard libraries
from contextvars import ContextVar
import logging
from os import environ
import re

# Third party libraries
import bugsnag


API_TOKEN: ContextVar[str] = ContextVar('API_TOKEN', default='')

STATIC_DIR: str = environ['SORTS_STATIC_PATH']

STAT_REGEX: re.Pattern = re.compile(
    r'([0-9]+ files? changed)?'
    r'(, (?P<insertions>[0-9]+) insertions\(\+\))?'
    r'(, (?P<deletions>[0-9]+) deletions\(\-\))?'
)
RENAME_REGEX: re.Pattern = re.compile(
    r'(?P<pre_path>.*)?'
    r'{(?P<old_name>.*) => (?P<new_name>.*)}'
    r'(?P<post_path>.*)?'
)

# Logging
LOGGER_HANDLER: logging.StreamHandler = logging.StreamHandler()
LOGGER: logging.Logger = logging.getLogger('Sorts')
LOGGER_REMOTE_HANDLER = bugsnag.handlers.BugsnagHandler()
LOGGER_REMOTE: logging.Logger = logging.getLogger('Sorts.stability')

MIXPANEL_API_TOKEN_SORTS = 'e7302b1c55ca87525a134eaef6a51d62'
