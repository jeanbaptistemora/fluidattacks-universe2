# pylint: disable=import-error

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.util import run_async

from ariadne.contrib.django.views import GraphQLView


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
