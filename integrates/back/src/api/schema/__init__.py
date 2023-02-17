from .enums import (
    ENUMS,
)
from .scalars import (
    SCALARS,
)
from .types import (
    TYPES,
)
from .unions import (
    UNIONS,
)
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from graphql import (
    GraphQLSchema,
)
import os

API_PATH = os.path.join(os.path.dirname(__file__), os.pardir)
SDL_CONTENT = "\n".join(
    [
        load_schema_from_path(f"{API_PATH}/interfaces"),
        load_schema_from_path(f"{API_PATH}/mutations"),
        load_schema_from_path(f"{API_PATH}/resolvers"),
        load_schema_from_path(f"{API_PATH}/schema"),
    ]
)

SCHEMA: GraphQLSchema = make_executable_schema(
    SDL_CONTENT,
    *ENUMS,
    *SCALARS,
    *TYPES,
    *UNIONS,
    snake_case_fallback_resolvers,
)
