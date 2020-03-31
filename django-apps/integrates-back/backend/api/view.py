import newrelic
from graphene_file_upload.django import FileUploadGraphQLView

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.middleware import ExecutorBackend


class APIView(FileUploadGraphQLView):
    graphiql_template = 'graphiql.html'

    # pylint: disable=too-many-arguments
    def execute_graphql_request(
            self, request, data, query, variables, operation_name,
            show_graphiql=False):
        name = operation_name if operation_name else 'External (unnamed)'
        newrelic.agent.set_transaction_name(f'api:{name}')
        newrelic.agent.add_custom_parameters(tuple(data.items()))

        return super(APIView, self).execute_graphql_request(
            request, data, query, variables, operation_name,
            show_graphiql=show_graphiql)

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
        options = {
            'backend': ExecutorBackend(),
            'graphiql': True,
        }
        options.update(kwargs)
        view = super(APIView, cls).as_view(**options)

        return view
