# Standard library
from typing import (
    Dict,
)
from urllib.parse import (
    quote_plus as url_encode,
)


def build_query(mapping: Dict[str, str]) -> str:
    return '&'.join({
        f'{url_encode(key)}={url_encode(val)}'
        for key, val in mapping.items()
    })
