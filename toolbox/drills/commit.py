# Standard library
import re
from typing import (
    Match,
    Optional,
)

# Third party libraries

# Local libraries
from toolbox import (
    logger,
)


def is_valid_msg(summary: str) -> bool:
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

    match: Optional[Match] = re.match(base_pattern, summary)
    if match and match.groupdict()['type'] == 'drills':
        logger.info('Pending to implement')
        is_valid = True
    else:
        logger.error(f'Drills commits begin must match: {base_pattern}')
        is_valid = False

    return is_valid


def is_drills_commit(summary: str) -> bool:
    return 'drills(' in summary
