# Standard library
import functools

# Local libraries
from toolbox import (
    constants,
    logger,
)


@functools.lru_cache(maxsize=None, typed=True)
def scan_exploit_for_kind_and_id(exploit_path: str) -> tuple:
    """Scan the exploit in search of metadata."""
    # /fin-1234-567890.exp        -> 567890, 'exp'
    # /fin-1234-567890.mock.exp   -> 567890, 'mock.exp'
    # /fin-1234-567890.cannot.exp -> 567890, 'cannot.exp'
    exploit_kind, finding_id = '', ''
    re_match = constants.RE_EXPLOIT_NAME.search(exploit_path)
    if re_match:
        finding_id, exploit_kind = re_match.groups()
    else:
        logger.warn('no kind or id found in', exploit_path)
    return exploit_kind, finding_id
