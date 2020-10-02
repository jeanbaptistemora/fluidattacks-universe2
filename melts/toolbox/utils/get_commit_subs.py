# Standard libraries
import re
from typing import Optional, Match
from functools import lru_cache

# Local libraries
from toolbox.utils import generic
from toolbox.utils.function import shield


@shield()
@lru_cache(maxsize=None, typed=True)
def main() -> str:
    """Return the group name from the last commmit msg."""
    group: str = ''

    summary: str = generic.get_change_request_summary()
    regex: str = r'\w+\(\w+\):\s+(?:#\d+(?:\.\d+)?\s+)?(?P<group>\w+)'

    regex_match: Optional[Match] = re.search(regex, summary)
    if regex_match:
        group = regex_match.groupdict()['group']

    return group
