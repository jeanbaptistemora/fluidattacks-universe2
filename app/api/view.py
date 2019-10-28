from django.conf import settings
from graphene_django.views import GraphQLView

from app.api.dataloaders.event import EventLoader
from app.api.dataloaders.finding import FindingLoader
from app.api.dataloaders.vulnerability import VulnerabilityLoader
from app.api.middleware import ExecutorBackend
from app.api.schema import SCHEMA


class APIView(GraphQLView):
    def get_context(self, request):
        """Appends dataloader instances to context"""
        context = super(APIView, self).get_context(request)
        context.loaders = {
            'event': EventLoader(),
            'finding': FindingLoader(),
            'vulnerability': VulnerabilityLoader()
        }

        return context

    @classmethod
    def as_view(cls, **kwargs):
        """Applies custom configs to the GraphQL view"""
        del kwargs
        options = {
            'backend': ExecutorBackend(),
            'graphiql': settings.DEBUG,
            'schema': SCHEMA
        }
        view = super(APIView, cls).as_view(**options)

        return view
