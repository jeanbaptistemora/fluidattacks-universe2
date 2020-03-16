# pylint: disable=import-error

from backend.domain import internal_project as internal_project_domain

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
def resolve_project_name(*_):
    """Resolve internalProjectNames query."""
    name = internal_project_domain.get_project_name()
    return dict(project_name=name)
