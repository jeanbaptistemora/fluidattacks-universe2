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
        f': '
        r'(?P<issue>#\d+)'
        r'\.'
        r'(?P<issue_part>[0-9]+)'
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
                logger.info('Commit type and scope: OK')
                is_valid = True
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
        else:
            logger.error(f'Generic commits must match: {generic_pattern}')
            is_valid = False
    else:
        logger.error(f'Commits begin must match: {base_pattern}')
        is_valid = False

    return is_valid
