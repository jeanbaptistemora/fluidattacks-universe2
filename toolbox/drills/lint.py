# Standard library
from glob import glob

# Third party libraries

# Local libraries
from toolbox import (
    logger
)


def check_folder_content():
    """Verify that drills do not contain forces code."""
    path_pattern = '*/drills/*/forces/'
    exploits = glob(path_pattern)
    if exploits:
        logger.error(('The drills folder must not contain code'
                      ' from forces, please relocate the following folders'))
        for exp in glob(path_pattern):
            logger.info(f'    {exp}')
        return False

    return True
