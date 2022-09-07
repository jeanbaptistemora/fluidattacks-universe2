# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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

SCHEMA_PATH: str = os.path.dirname(os.path.abspath(__file__))
SDL_CONTENT: str = load_schema_from_path(SCHEMA_PATH)

SCHEMA: GraphQLSchema = make_executable_schema(
    SDL_CONTENT,
    *ENUMS,
    *SCALARS,
    *TYPES,
    *UNIONS,
    snake_case_fallback_resolvers,
)
