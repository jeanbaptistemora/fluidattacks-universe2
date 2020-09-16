# Standard library
from os import environ
import os
from typing import (
    Literal,
    Union,
)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def guess_environment(
) -> Union[Literal['development'], Literal['production'], ]:
    if any((
            'product/' in BASE_DIR,
            environ.get('CI_COMMIT_REF_NAME', 'master') != 'master',
    )):
        return 'development'

    return 'production'
