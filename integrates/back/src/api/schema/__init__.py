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
from ariadne.validation import (
    cost_directive,
)
from graphql import (
    GraphQLSchema,
)
import os

SCHEMA_PATH: str = os.path.dirname(os.path.abspath(__file__))
SDL_CONTENT: str = load_schema_from_path(SCHEMA_PATH)

SCHEMA: GraphQLSchema = make_executable_schema(
    [SDL_CONTENT, cost_directive],
    *ENUMS,
    *SCALARS,
    *TYPES,
    *UNIONS,
    snake_case_fallback_resolvers,
)
