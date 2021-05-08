# Standard libraries
from typing import Any

# Local libraries
from custom_exceptions import InvalidSource


def get_source(context: Any) -> str:
    headers = context.headers
    source = headers.get('x-integrates-source', 'integrates')
    if source not in {'integrates', 'skims'}:
        raise InvalidSource()
    return source
