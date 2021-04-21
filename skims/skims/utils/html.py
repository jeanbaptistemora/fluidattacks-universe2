# Standard library
from string import (
    whitespace,
)

# Third party libraries
from bs4 import (
    BeautifulSoup,
)


def is_html(string: str) -> bool:
    string = string.strip(whitespace)

    if string.startswith('{'):
        # JSON
        return False

    soup = BeautifulSoup(string, 'html.parser')

    return soup.find('html', recursive=False) is not None
