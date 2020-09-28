# Standard library
from os import environ
from typing import (
    Literal,
    Union,
)

# Local libraries
from utils.ctx import (
    ROOT,
)


def guess_environment() -> Union[
    Literal['development'],
    Literal['production'],
]:
    if any((
        'product' in ROOT,
        environ.get('CI_COMMIT_REF_NAME', 'master') != 'master',
    )):
        return 'development'

    return 'production'
