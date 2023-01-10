from enum import (
    Enum,
)
from os import (
    environ,
)


class BinPaths(Enum):
    DETERMINE_SCHEMAS = environ["DYNAMO_DETERMINE_SCHEMA"]
    PREPARE_LOADING = environ["DYNAMO_PREPARE_LOADING"]
