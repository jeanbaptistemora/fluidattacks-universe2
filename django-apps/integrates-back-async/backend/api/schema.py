# pylint: disable=import-error

import os

from backend.api.query import QUERY, ME
from backend.api.mutation import MUTATION
from backend.api.typesdef import TYPES
from backend.api.scalars import jsonstring, genericscalar, datetime

from ariadne import (
    make_executable_schema, load_schema_from_path, upload_scalar,
    snake_case_fallback_resolvers
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TYPE_DEFS = load_schema_from_path(os.path.join(BASE_DIR, 'api', 'schemas'))

SCHEMA = make_executable_schema(
    TYPE_DEFS,
    QUERY,
    ME,
    MUTATION,
    *TYPES,
    jsonstring.JSON_STRING_SCALAR,
    genericscalar.GENERIC_SCALAR,
    datetime.DATETIME_SCALAR,
    upload_scalar,
    snake_case_fallback_resolvers
)
