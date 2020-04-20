# Standard libraries
import re
from typing import Optional, Match
from functools import lru_cache

# Local libraries
from toolbox.utils import generic


@lru_cache(maxsize=None, typed=True)
def main() -> str:
    """Return the subscription name from the last commmit msg."""
    subscription: str = ''

    summary: str = generic.get_change_request_summary()
    regex: str = r'\w+\(\w+\):\s+(?:#\d+(?:\.\d+)?\s+)?(?P<subscription>\w+)'

    regex_match: Optional[Match] = re.search(regex, summary)
    if regex_match:
        subscription = regex_match.groupdict()['subscription']

    return subscription
