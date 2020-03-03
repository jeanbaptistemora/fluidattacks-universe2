# pylint: disable=import-error

from ariadne import (
    make_executable_schema, load_schema_from_path, upload_scalar,
    snake_case_fallback_resolvers
)

from backend.api.entity.query import QUERY
from backend.api.entity.alert import ALERT
from backend.api.entity.event import EVENT
from backend.api.entity.finding import FINDING
from backend.api.entity.internal_project import INTERNAL_PROJECT_NAME
from backend.api.entity.resource import RESOURCE
from backend.api.entity.user import USER
from backend.api.entity.project import PROJECT
from backend.api.entity.break_build import BREAK_BUILD_EXECUTIONS
from backend.api.entity.me import ME
from backend.api.scalars import datetime, jsonstring, genericscalar


TYPE_DEFS = load_schema_from_path('schemas/')

SCHEMA = make_executable_schema(
    TYPE_DEFS,
    [
        QUERY,
        ALERT,
        EVENT,
        FINDING,
        INTERNAL_PROJECT_NAME,
        RESOURCE,
        USER,
        PROJECT,
        BREAK_BUILD_EXECUTIONS,
        ME,
        datetime.DATETIME_SCALAR,
        jsonstring.JSON_STRING_SCALAR,
        genericscalar.GENERIC_SCALAR,
        upload_scalar
    ],
    snake_case_fallback_resolvers
)
