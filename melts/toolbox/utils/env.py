# Standard library
from os import environ

# local libraries
from toolbox.constants import BASE_DIR


def guess_environment(
) -> str:
    if any((
        'product/' in BASE_DIR,
        environ.get('CI_COMMIT_REF_NAME', 'master') != 'master',
    )):
        return 'development'

    return 'production'  # pragma: no cover
