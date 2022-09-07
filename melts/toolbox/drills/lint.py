# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from glob import (
    glob,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils.function import (
    shield,
)


@shield(retries=1)
def check_folder_content() -> bool:
    """Verify that drills do not contain forces code."""
    path_pattern = "*/drills/*/forces/"
    exploits = glob(path_pattern)
    success = True

    if exploits:
        LOGGER.error(
            (
                "The drills folder must not contain code"
                " from forces, please relocate the following folders"
            )
        )
        for exp in exploits:
            LOGGER.info("    %s", exp)
        success = False

    return success
