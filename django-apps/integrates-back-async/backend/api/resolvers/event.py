# pylint: disable=import-error

from ariadne import convert_kwargs_to_snake_case
from backend.domain import event as event_domain


@convert_kwargs_to_snake_case
def resolve_event(*_, identifier):
    """Resolve event query."""
    return event_domain.get_event(identifier)
