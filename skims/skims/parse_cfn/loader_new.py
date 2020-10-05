# Standard library
from typing import (
    Any,
)

# Third party libraries
from metaloaders import (
    json,
    yaml,
)
from aioextensions import (
    in_process, )


async def load(content: str, fmt: str) -> Any:
    if fmt in {'yml', 'yaml'}:
        return await in_process(yaml.load, content)

    if fmt in {'json'}:
        return await in_process(json.load, content)

    return {}
