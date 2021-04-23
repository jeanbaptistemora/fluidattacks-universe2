# Standard library
import os
from typing import (
    Dict,
    Tuple,
)

# Local libraries
from parse_java_properties import (
    load_as_dict,
)


def load(paths: Tuple[str, ...]) -> Dict[str, Dict[str, str]]:
    resources: Dict[str, Dict[str, str]] = {}

    for path in paths:
        if path.endswith(".properties"):
            with open(path) as handle:
                resources[os.path.basename(path)] = load_as_dict(handle.read())

    return resources
