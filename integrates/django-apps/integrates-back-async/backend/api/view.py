# pylint: disable=not-callable
from collections import defaultdict
from typing import cast

import newrelic
from django.conf import settings
from django.http import HttpRequest
from graphql import GraphQLSchema
from ariadne.contrib.django.views import GraphQLView
from ariadne.format_error import format_error
from ariadne.types import GraphQLResult
from ariadne import graphql

from asgiref.sync import async_to_sync
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.single_vulnerability import (
    SingleVulnerabilityLoader
)
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend import util


def append_context_value(context):
    """Add dataloaders to context async."""
    context.loaders = {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'group': GroupLoader(),
        'group_drafts': GroupDraftsLoader(),
        'group_findings': GroupFindingsLoader(),
        'project': ProjectLoader(),
        'single_vulnerability': SingleVulnerabilityLoader(),
        'vulnerability': VulnerabilityLoader(),
    }
    context.store = defaultdict(lambda: None)

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

        return append_context_value(context)

    async def _execute(
            self, request: HttpRequest, data: dict) -> GraphQLResult:
        """Execute query"""

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
        """Execute async query and apply configs for performance tracking"""
        name = data.get('operationName', 'External (unnamed)')
        variables = data.get('variables', '-')
        query = data.get('query', '-').replace('\n', '')
        newrelic.agent.set_transaction_name(f'api:{name}')
        newrelic.agent.add_custom_parameters(tuple(data.items()))
        util.cloudwatch_log_sync(
            request,
            f'API: {name} with parameters {variables}. Complete query: {query}'
        )

        # Use this instead of asyncio.run
        # https://docs.djangoproject.com/en/3.0/topics/async/#async-to-sync
        # https://stackoverflow.com/questions/59503825/django-async-to-sync-vs-asyncio-run
        return async_to_sync(self._execute)(request, data)
