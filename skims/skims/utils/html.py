# Standard library
from string import (
    whitespace,
)
from typing import (
    Optional,
)

# Third party libraries
from bs4 import (
    BeautifulSoup,
)


def is_html(string: str, soup: Optional[BeautifulSoup] = None) -> bool:
    string = string.strip(whitespace)

    if string.startswith('{'):
        # JSON
        return False

    if soup is None:
        soup = BeautifulSoup(string, 'html.parser')

    return soup.find('html', recursive=False) is not None
