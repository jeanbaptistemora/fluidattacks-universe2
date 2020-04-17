# Standard library
import functools
import re

# Local libraries
from toolbox import utils


RE_COMMIT_MSG = re.compile(r'drills\(\w+\):\s+(\w+)')


@functools.lru_cache(maxsize=None, typed=True)
def main() -> bool:
    """Return True if the last commit in git history commit has drills type."""
    commit_msg: str = utils.get_commit_message()
    return bool(RE_COMMIT_MSG.search(commit_msg))
