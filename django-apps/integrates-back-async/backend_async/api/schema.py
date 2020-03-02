# pylint: disable=import-error

from ariadne import (
    make_executable_schema, load_schema_from_path, upload_scalar
)

from backend_async.api.entity.query import QUERY
from backend_async.api.entity.alert import ALERT
from backend_async.api.entity.event import EVENT
from backend_async.api.entity.finding import FINDING
from backend_async.api.entity.internal_project import INTERNAL_PROJECT_NAME
from backend_async.api.entity.resource import RESOURCE
from backend_async.api.entity.user import USER
from backend_async.api.entity.project import PROJECT
from backend_async.api.entity.break_build import BREAK_BUILD_EXECUTIONS
from backend_async.api.entity.me import ME
from backend_async.api.scalars import datetime, jsonstring, genericscalar


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
    ]
)
