import os
from parse_java_properties import (
    load_as_dict,
)
from typing import (
    Dict,
    Tuple,
)


def load(paths: Tuple[str, ...]) -> Dict[str, Dict[str, str]]:
    resources: Dict[str, Dict[str, str]] = {}

    for path in paths:
        if path.endswith(".properties"):
            with open(path, encoding="utf-8") as handle:
                resources[os.path.basename(path)] = load_as_dict(handle.read())

    return resources
