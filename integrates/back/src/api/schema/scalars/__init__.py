from typing import Tuple

from ariadne import (
    ScalarType,
    upload_scalar,
)

from .datetime import DATETIME_SCALAR
from .genericscalar import GENERIC_SCALAR
from .jsonstring import JSON_STRING_SCALAR


SCALARS: Tuple[ScalarType, ...] = (
    JSON_STRING_SCALAR,
    GENERIC_SCALAR,
    DATETIME_SCALAR,
    upload_scalar,
)
