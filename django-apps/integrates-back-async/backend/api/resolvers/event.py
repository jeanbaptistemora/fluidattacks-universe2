# pylint: disable=import-error

from ariadne import convert_kwargs_to_snake_case
from backend.domain import event as event_domain
from backend.domain import project as project_domain
from backend import util


@convert_kwargs_to_snake_case
def resolve_event(*_, identifier):
    """Resolve event query."""
    return event_domain.get_event(identifier)


@convert_kwargs_to_snake_case
def resolve_events(_, info, project_name):
    """Resolve events query."""
    util.cloudwatch_log(
        info.context, f'Security: Access to {project_name} events')
    event_ids = project_domain.list_events(project_name)
    events_loader = info.context.loaders['event']
    return events_loader.load_many(event_ids)
