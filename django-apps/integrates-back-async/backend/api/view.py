# pylint: disable=import-error

from ariadne.contrib.django.views import GraphQLView


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
