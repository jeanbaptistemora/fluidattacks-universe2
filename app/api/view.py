from django.conf import settings
from graphene_django.views import GraphQLView

from app.api.middleware import blacklist_middleware, ExecutorBackend
from app.api.schema import SCHEMA


class APIView(GraphQLView):
    def get_context(self, request):
        """Appends dataloader instances to context"""
        context = super(APIView, self).get_context(request)
        context.vulnerabilities_loader = {}

        return context

    @classmethod
    def as_view(cls, **kwargs):
        """Applies custom configs to the GraphQL view"""
        del kwargs
        options = {
            'backend': ExecutorBackend(),
            'graphiql': settings.DEBUG,
            'middleware': [
                blacklist_middleware
            ],
            'schema': SCHEMA
        }
        view = super(APIView, cls).as_view(**options)

        return view
