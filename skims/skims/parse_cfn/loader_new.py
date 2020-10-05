# Standard library
from typing import (
    Any,
)

# Third party libraries
from metaloaders import (
    json,
    yaml,
)
from metaloaders.model import Type
from aioextensions import (
    in_process, )


async def load(content: str, fmt: str) -> Any:
    if fmt in {'yml', 'yaml'}:
        template = await in_process(yaml.load, content)
        if template.data_type == Type.ARRAY:
            return template.data[0]
        return template

    if fmt in {'json'}:
        return await in_process(json.load, content)

    return {}
