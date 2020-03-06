# pylint: disable=import-error

from ariadne import convert_kwargs_to_snake_case
from backend.domain import internal_project as internal_project_domain


@convert_kwargs_to_snake_case
def resolve_project_name(*_):
    """Resolve internalProjectNames query."""
    return internal_project_domain.get_project_name()
