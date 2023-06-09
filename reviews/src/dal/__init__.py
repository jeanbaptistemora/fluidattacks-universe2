from dal.model import (
    MissingEnvironmentVariable,
)
import os
from utils.logs import (
    log,
)


def verify_required_vars(variables: list[str]) -> None:
    success: bool = True
    for variable in variables:
        if variable not in os.environ:
            success = False
            log("error", "%s must be set", variable)
    if not success:
        raise MissingEnvironmentVariable
