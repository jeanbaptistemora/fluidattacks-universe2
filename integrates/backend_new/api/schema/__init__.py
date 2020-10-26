# Graphql schema declaration

# Standard library
import os

# Third party libraries
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers
)
from graphql import GraphQLSchema

# Local libraries
from backend.api.schema.enums import ENUMS
from backend.api.schema.scalars import SCALARS
from backend.api.schema.types import TYPES


SCHEMA_PATH: str = os.path.dirname(
    os.path.abspath(__file__).replace(
        'backend_new/', 'django-apps/integrates-back-async/backend/'
    ).replace('schema.py', 'schema/__init__.py')
)
SDL_CONTENT: str = load_schema_from_path(SCHEMA_PATH)

SCHEMA: GraphQLSchema = make_executable_schema(
    SDL_CONTENT,
    *ENUMS,
    *SCALARS,
    *TYPES,
    snake_case_fallback_resolvers
)
