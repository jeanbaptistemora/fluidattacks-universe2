# Standard libraries
import os
from typing import List, Any

# Third party libraries
from gitlab import Gitlab

# Local libraries
import dal.gitlab
from utils.logs import log


def verify_required_vars(variables: List[str]) -> bool:
    success: bool = True
    for variable in variables:
        if variable not in os.environ:
            success = False
            log('error',
                '%s must be set',
                variable)
    return success
