# Standard library
from typing import (
    Set,
)

# Local imports
from parse_tree_sitter.parse import (
    get_root,
)
from utils.ctx import (
    CTX,
)
from utils.fs import (
    resolve_paths,
)


async def analyze(
) -> None:
    unique_paths: Set[str] = await resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )

    await get_root(tuple(unique_paths))
