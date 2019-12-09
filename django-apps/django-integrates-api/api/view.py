from graphene_file_upload.django import FileUploadGraphQLView

from api.dataloaders.event import EventLoader
from api.dataloaders.finding import FindingLoader
from api.dataloaders.vulnerability import VulnerabilityLoader
from api.middleware import ExecutorBackend
from api.schema import SCHEMA


class APIView(FileUploadGraphQLView):
    graphiql_template = 'graphiql.html'

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
            'graphiql': True,
            'schema': SCHEMA
        }
        view = super(APIView, cls).as_view(**options)

        return view
