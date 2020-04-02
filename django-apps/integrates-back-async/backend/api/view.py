# pylint: disable=import-error

import newrelic

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.util import run_async

from django.http import HttpRequest
from ariadne.contrib.django.views import GraphQLView
from ariadne.types import GraphQLResult


async def _context_value(context):
    """Add dataloaders to context async."""
    context.loaders = {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'vulnerability': VulnerabilityLoader()
    }
    return context


# pylint: disable=too-few-public-methods
class APIView(GraphQLView):

    @classmethod
    def as_view(cls, **kwargs):
        """Apply custom configs to the GraphQL view."""
        options = {
            'playground_options': {
                'request.credentials': 'include'
            },
        }
        options.update(kwargs)
        view = super(APIView, cls).as_view(**options)

        return view

    def context_value(self, request):
        """Add dataloaders to context."""
        if callable(super().context_value):
            context = super().context_value(request)
        else:
            context = super().context_value or request
        return run_async(_context_value, context)

    def execute_query(self, request: HttpRequest, data: dict) -> GraphQLResult:
        """ Apply configs for performance tracking """
        name = data.get('operationName', 'External (unnamed)')
        newrelic.agent.set_transaction_name(f'v2/api:{name}')
        newrelic.agent.add_custom_parameters(tuple(data.items()))

        return super(APIView, self).execute_query(request, data)
