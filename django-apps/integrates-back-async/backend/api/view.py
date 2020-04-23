# pylint: disable=not-callable
import asyncio

from typing import cast

import newrelic

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader

from django.conf import settings
from django.http import HttpRequest
from graphql import GraphQLSchema
from ariadne.contrib.django.views import GraphQLView
from ariadne.format_error import format_error
from ariadne.types import GraphQLResult
from ariadne import graphql


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

    async def context_value(self, request):
        """Add dataloaders to context."""
        if callable(super().context_value):
            context = \
                super().context_value(request)  # pylint: disable=not-callable
        else:
            context = super().context_value or request
        return await _context_value(context)

    async def _execute(
            self, request: HttpRequest, data: dict) -> GraphQLResult:
        """Apply configs for performance tracking."""
        name = data.get('operationName', 'External (unnamed)')
        newrelic.agent.set_transaction_name(f'v2/api:{name}')
        newrelic.agent.add_custom_parameters(tuple(data.items()))

        if callable(self.context_value):
            context_value = \
                await self.context_value(request)
        else:
            context_value = self.context_value or request

        return await graphql(
            cast(GraphQLSchema, self.schema),
            data,
            context_value=context_value,
            root_value=self.root_value,
            debug=settings.DEBUG,
            logger=self.logger,
            validation_rules=self.validation_rules,
            error_formatter=self.error_formatter or format_error,
            middleware=self.middleware,
        )

    def execute_query(self, request: HttpRequest, data: dict) -> GraphQLResult:
        """Execute async query."""
        return asyncio.run(self._execute(request, data))
