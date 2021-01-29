# Standard library
import operator
import re
from typing import (
    Match,
    Optional,
    Tuple,
)

# Third party libraries

# Local libraries
from toolbox import (
    utils,
)
from toolbox.logger import LOGGER
from toolbox.utils.function import shield


VALID__SCOPES_DESC: Tuple[Tuple[str, str], ...] = (
    ('front', 'Front-End change'),
    ('back', 'Back-End change'),
    ('infra', 'Infrastructure change'),
    ('conf', 'Configuration files change'),
    ('build', 'Build system, CI, compilers, etc'),
    ('job', 'CI or schedule tasks (backups, maintenance, etc)'),
    ('doc', 'Documentation only changes'),
    ('cross', 'Mix of two or more scopes'),
)
VALID__TYPES_DESC: Tuple[Tuple[str, str], ...] = (
    ('rever', 'Revert to a previous commit in history'),
    ('feat', 'New feature, improvement, enhancement'),
    ('perf', 'Improves resource consumption (time/space)'),
    ('fix', 'Someone (or you) did wrong, you are getting things right'),
    ('refac', 'Neither fixes a bug or adds a feature'),
    ('test', 'Adding missing tests or correcting existing tests'),
    ('style', 'Do not affect the meaning of the code (formatting, etc)'),
)

VALID_SCOPES: Tuple[str, ...] = \
    tuple(map(operator.itemgetter(0), VALID__SCOPES_DESC))
VALID_TYPES: Tuple[str, ...] = \
    tuple(map(operator.itemgetter(0), VALID__TYPES_DESC))


@shield()
def has_short_line_length(summary: str, body: str) -> bool:
    """Verify that summary and body are below max chars threshold."""
    success: bool = True

    if any(len(summary_line) > 50 for summary_line in summary.splitlines()):
        LOGGER.error('Summary too long, 50 chars max')
        success = False

    if any(len(body_line) > 72 for body_line in body.splitlines()):
        LOGGER.error('Body lines too long, 72 chars max')
        success = False

    return success


@shield()
def is_under_100_deltas(ref: str = 'HEAD') -> bool:
    """Return True if the HEAD commit is under 100 deltas."""
    skip_check: bool = \
        '- no-deltas-check' in utils.generic.get_change_request_body(ref)

    if skip_check:
        LOGGER.info('Deltas check skipped')
        return True

    request_deltas: int = utils.generic.get_change_request_deltas(ref)
    if request_deltas > 100:
        LOGGER.error('Your commit has more than 100 deltas: %i',
                     request_deltas)
        return False

    return True


@shield()
def is_valid_summary(summary: str) -> bool:
    """Plugable validator for forces commits."""
    is_valid: bool = True

    # xxx(yyy)
    base_pattern: str = (
        r'^'
        r'(?P<type>[a-z]+)'
        r'\('
        r'(?P<scope>[a-z]+)'
        r'\)'
    )
    # fix(back): #123.1 comment, continuted
    generic_pattern = base_pattern + (
        ': '
        r'(?P<issue>#[1-9]\d*)'
        r'\.'
        r'(?P<issue_part>[1-9]\d*)'
        r' '
        r'(?P<comment>[a-z, _-]+)'
        r'$'
    )

    match: Optional[Match] = re.match(base_pattern, summary)
    if match:
        match = re.match(generic_pattern, summary)
        if match:
            type_: str = match.groupdict()['type']
            scope: str = match.groupdict()['scope']

            if type_ in VALID_TYPES and scope in VALID_SCOPES:
                LOGGER.info('Commit type and scope: OK')
                is_valid = True
            else:
                LOGGER.error('Provide a valid commit type(scope)')
                LOGGER.info('Yours is: %s(%s)', type_, scope)
                LOGGER.info('Valid types are:')
                for type_, desc in VALID__TYPES_DESC:
                    LOGGER.info('  - %s: %s', type_, desc)
                LOGGER.info('Valid scopes are:')
                for scope, desc in VALID__SCOPES_DESC:
                    LOGGER.info('  - %s: %s', scope, desc)
                is_valid = False
        else:
            LOGGER.error('Generic commits must match: %s', generic_pattern)
            is_valid = False
    else:
        LOGGER.error('Commits begin must match: %s', base_pattern)
        is_valid = False

    return is_valid
