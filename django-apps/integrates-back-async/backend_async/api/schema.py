# pylint: disable=import-error

from ariadne import make_executable_schema, load_schema_from_path

from backend_async.api.entity.query import QUERY
from backend_async.api.entity.alert import ALERT
from backend_async.api.entity.event import EVENT
from backend_async.api.entity.finding import FINDING
from backend_async.api.entity.internal_project import INTERNAL_PROJECT_NAMES
from backend_async.api.entity.resource import RESOURCE
from backend_async.api.entity.user import USER
from backend_async.api.entity.project import PROJECT
from backend_async.api.entity.break_build import BREAK_BUILD_EXECUTIONS
from backend_async.api.entity.me import ME


TYPE_DEFS = load_schema_from_path('schemas/')

SCHEMA = make_executable_schema(
    TYPE_DEFS,
    [
        QUERY,
        ALERT,
        EVENT,
        FINDING,
        INTERNAL_PROJECT_NAMES,
        RESOURCE,
        USER,
        PROJECT,
        BREAK_BUILD_EXECUTIONS,
        ME,
    ]
)
