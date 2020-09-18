# Standard
import os

# Third party
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers
)
from graphql import GraphQLSchema

# Local
from backend.api.schema.enums import ENUMS
from backend.api.schema.scalars import SCALARS
from backend.api.schema.types import TYPES


SCHEMA_PATH: str = os.path.dirname(os.path.abspath(__file__))
SDL_CONTENT: str = load_schema_from_path(SCHEMA_PATH)

SCHEMA: GraphQLSchema = make_executable_schema(
    SDL_CONTENT,
    *ENUMS,
    *SCALARS,
    *TYPES,
    snake_case_fallback_resolvers
)
