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
    logger,
)

VALID__SCOPES_DESC: Tuple[Tuple[str, str], ...] = (
    ('enum', 'Enumeration of ToE without testing'),
    ('conf', 'Configuration files change'),
    ('cross', 'Comprehensive (lines and inputs) testing'),
    ('lines', 'Source code testing'),
    ('inputs', 'Environment/App/Machine testing'),
)
VALID__TYPES_DESC: Tuple[Tuple[str, str], ...] = (
    ('drills', 'Drills service related commit'),
)

VALID_SCOPES: Tuple[str, ...] = \
    tuple(map(operator.itemgetter(0), VALID__SCOPES_DESC))
VALID_TYPES: Tuple[str, ...] = \
    tuple(map(operator.itemgetter(0), VALID__TYPES_DESC))
VALID_REASONS: Tuple[str, ...] = \
    tuple(map(lambda r: f'not-drills(cross)-because: {r}', (
        'i-already-tested-all-lines',
        'i-already-tested-all-inputs',
        'i-was-increasing-lines-coverage',
        'i-was-increasing-inputs-coverage',
        'toe-has-lines-only',
        'there-is-a-lines-eventuality',
        'there-is-an-inputs-eventuality',
        'inputs-have-no-corresponding-lines',
        'i-think-lines-have-more-vulns-than-inputs',
        'i-think-inputs-have-more-vulns-than-lines',
        'other: <please specify here>',
    )))


def is_valid_summary(  # pylint: disable=too-many-statements,too-many-branches
    summary: str,
    body: str = str(),
) -> bool:
    """Plugable validator for drills commits."""
    is_valid: bool = True

    # xxx(yyy)
    base_pattern: str = (
        r'^'
        r'(?P<type>[a-z]+)'
        r'\('
        r'(?P<scope>[a-z]+)'
        r'\)'
    )
    # drills(lines/inputs/cross): continuoustest - 72.75%, 0 el, 6 ei
    daily_pattern: str = base_pattern + (
        r': '
        r'(?P<group>[a-z0-9]+)'
        r' - '
        r'(?P<coverage>\d+\.\d{2}%)'
        r', '
        r'(?P<evaluated_lines>\d+) el'
        r', '
        r'(?P<evaluated_inputs>\d+) ei'
        r'$'
    )
    # drills(enum): continuoustest - 0 nl, 3ni
    enum_pattern: str = base_pattern + (
        r': '
        r'(?P<group>[a-z0-9]+)'
        r' - '
        r'(?P<new_lines>\d+) nl'
        r', '
        r'(?P<new_inputs>\d+) ni'
        r'$'
    )
    # drills(conf): continuoustest - comment, continued
    config_pattern = base_pattern + (
        f': '
        r'(?P<group>[a-z0-9]+)'
        r' - '
        r'(?P<comment>[a-z, _-]+)'
        r'$'
    )

    match: Optional[Match] = re.match(base_pattern, summary)
    match_groups = match.groupdict() if match else {}
    type_: str = match_groups.get('type', '')
    scope: str = match_groups.get('scope', '')
    if match and type_ in VALID_TYPES and scope in VALID_SCOPES:
        if type_ == 'drills' and scope in ('lines', 'inputs', 'cross'):
            match = re.match(daily_pattern, summary)
            if match:
                if scope == 'cross' \
                        or any(reason in body for reason in VALID_REASONS):
                    logger.info('Drills daily commit: OK')
                    is_valid = True
                else:
                    logger.error('Provide a valid reason for non-cross hack')
                    logger.info(f'Valid reasons are:')
                    for reason in VALID_REASONS:
                        logger.info(f'  - {reason}')
                    is_valid = False
            else:
                logger.error(f'Daily commit must match: {daily_pattern}')
                is_valid = False
        elif type_ == 'drills' and scope == 'enum':
            match = re.match(enum_pattern, summary)
            if match:
                logger.info('Drills enumeration commit: OK')
                is_valid = True
            else:
                logger.error(f'Enumeration commit must match: {enum_pattern}')
                is_valid = False
        elif type_ == 'drills' and scope == 'conf':
            match = re.match(config_pattern, summary)
            if match:
                logger.info('Drills config commit: OK')
                is_valid = True
            else:
                logger.error(f'Config commit must match: {config_pattern}')
                is_valid = False
        else:
            logger.error(f'Unrecognized scope: {type_}({scope})')
            is_valid = False
    else:
        logger.error('Provide a valid commit type(scope)')
        logger.info(f'Yours is: {type_}({scope})')
        logger.info(f'Valid types are:')
        for type_, desc in VALID__TYPES_DESC:
            logger.info(f'  - {type_}: {desc}')
        logger.info(f'Valid scopes are:')
        for scope, desc in VALID__SCOPES_DESC:
            logger.info(f'  - {scope}: {desc}')
        is_valid = False

    return is_valid


def is_drills_commit(summary: str) -> bool:
    return 'drills(' in summary
