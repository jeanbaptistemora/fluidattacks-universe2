# Local libraries
from toolbox.utils import generic
from toolbox.logger import LOGGER


def main(subs: str) -> bool:
    """Return True if the group exists."""
    if generic.does_subs_exist(subs):
        return True
    LOGGER.error('"%s" is not an existing group.', subs)
    return False
