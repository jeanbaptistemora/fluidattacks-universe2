# Standard
from collections import defaultdict

# Third party
import newrelic.agent
from ariadne.asgi import GraphQL
from django.utils.decorators import method_decorator

# Local
from backend import util
from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader


class IntegratesAPI(GraphQL):
    async def get_context_for_request(self, request):
        context = request
        context.loaders = {
            'event': EventLoader(),
            'finding': FindingLoader(),
            'finding_vulns': FindingVulnsLoader(),
            'group': GroupLoader(),
            'group_drafts': GroupDraftsLoader(),
            'group_findings': GroupFindingsLoader(),
            'vulnerability': VulnerabilityLoader()
        }
        context.store = defaultdict(lambda: None)

        return context

    async def extract_data_from_request(self, request):
        """Apply configs for performance tracking"""
        data = await super().extract_data_from_request(request)

        name = data.get('operationName', 'External (unnamed)')
        query = data.get('query', '-').replace('\n', '')
        variables = data.get('variables', '-')

        newrelic.agent.set_transaction_name(f'api:{name}')
        newrelic.agent.add_custom_parameters(tuple(data.items()))
        await util.cloudwatch_log_async(
            request,
            f'API: {name} with parameters {variables}. Complete query: {query}'
        )

        return data

    @method_decorator(newrelic.agent.web_transaction())
    async def graphql_http_server(self, request):
        return await super().graphql_http_server(request)
