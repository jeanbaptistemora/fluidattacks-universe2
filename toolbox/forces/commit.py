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
    # feat(exp): subs
    regular_pattern = base_pattern + (
        f': '
        r'(?P<subscription>[a-z]+)'
        r'$'
    )
    # fix(exp): #123 subs tag
    fix_pattern = base_pattern + (
        f': '
        r'(?P<issue>#[1-9]\d*)'
        r' '
        r'(?P<subscription>[a-z]+)'
        r' '
        r'(?P<mod_reason>[a-z-]+)'
        r'$'
    )
    mods__reason_desc: Tuple[Tuple[str, str], ...] = (
        ('asserts-ch',
         'Change in a product, for instance Fluidasserts'),
        ('asserts-fn',
         'False negative in a product'),
        ('asserts-fp',
         'False positive in a product'),
        ('service-logic',
         'Error in exploit construction'),
        ('toe-availability',
         'If the ToE is no longer reachable or available'),
        ('toe-location',
         'Change in the ToE, like path deletion/movement, etc'),
        ('toe-resource',
         'Change in the environment, like renaming or deletion'),
    )
    mod_reasons: Tuple[str, ...] = \
        tuple(map(operator.itemgetter(0), mods__reason_desc))

    match: Optional[Match] = re.match(base_pattern, summary)
    if match and match.groupdict()['scope'] == 'exp':
        if match.groupdict()['type'] == 'fix':
            match = re.match(fix_pattern, summary)
            if match:
                mod_reason: str = match.groupdict()['mod_reason']

                if mod_reason in mod_reasons:
                    logger.info('Modification reason Ok')
                    is_valid = True
                else:
                    logger.error('Provide a valid modification reason')
                    logger.info(f'Yours is: {mod_reason}')
                    logger.info(f'Valid ones are:')
                    for mod_reason, desc in mods__reason_desc:
                        logger.info(f'  - {mod_reason}: {desc}')
                    is_valid = False
            else:
                logger.error(f'fix(exp) commits must match: {fix_pattern}')
                is_valid = False
        else:
            match = re.match(regular_pattern, summary)
            if match:
                logger.info('Commit msg is ok')
                is_valid = True
            else:
                logger.error(f'xxx(exp) commits must match: {regular_pattern}')
                is_valid = False
    else:
        logger.error(f'Exploits commits begin must match: {base_pattern}')
        is_valid = False

    return is_valid


def is_exploits_commit(summary: str) -> bool:
    """Return True if this is a forces commit."""
    return '(exp)' in summary
