# pylint: disable=import-error

import os

from ariadne import (
    make_executable_schema, load_schema_from_path, upload_scalar,
    snake_case_fallback_resolvers
)

from backend.api.query import QUERY
from backend.api.typesdef import TYPES
from backend.api.scalars import datetime, jsonstring, genericscalar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TYPE_DEFS = load_schema_from_path(os.path.join(BASE_DIR, 'api', 'schemas'))

SCHEMA = make_executable_schema(
    TYPE_DEFS,
    QUERY,
    *TYPES,
    datetime.DATETIME_SCALAR,
    jsonstring.JSON_STRING_SCALAR,
    genericscalar.GENERIC_SCALAR,
    upload_scalar,
    snake_case_fallback_resolvers
)
