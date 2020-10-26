# Standard
from typing import Tuple

# Third party
from ariadne import ScalarType, upload_scalar

# Local
from backend.api.schema.scalars.datetime import DATETIME_SCALAR
from backend.api.schema.scalars.genericscalar import GENERIC_SCALAR
from backend.api.schema.scalars.jsonstring import JSON_STRING_SCALAR

SCALARS: Tuple[ScalarType, ...] = (
    JSON_STRING_SCALAR,
    GENERIC_SCALAR,
    DATETIME_SCALAR,
    upload_scalar
)
