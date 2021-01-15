# Standard library
from glob import glob

# Third party libraries

# Local libraries
from toolbox import (
    logger
)
from toolbox.utils.function import shield


@shield(retries=1)
def check_folder_content() -> bool:
    """Verify that drills do not contain forces code."""
    path_pattern = '*/drills/*/forces/'
    exploits = glob(path_pattern)
    success = True

    if exploits:
        logger.error(('The drills folder must not contain code'
                      ' from forces, please relocate the following folders'))
        for exp in exploits:
            logger.info(f'    {exp}')
        success = False

    return success
