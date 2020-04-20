# Standard libraries
from glob import glob

# Local libraries
from toolbox import logger


def main(subs: str) -> bool:
    """Return True if the subscription exists."""
    if f'subscriptions/{subs}' in glob('subscriptions/*'):
        return True
    logger.error(f'"{subs}" is not an existing subscription.')
    return False
