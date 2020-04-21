# Local libraries
from toolbox.utils import generic
from toolbox import logger


def main(subs: str) -> bool:
    """Return True if the subscription exists."""
    if generic.does_subs_exist(subs):
        return True
    logger.error(f'"{subs}" is not an existing subscription.')
    return False
