from ariadne import graphql

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.single_vulnerability import (
    SingleVulnerabilityLoader
)
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from test_async.utils import create_dummy_session


async def get_result(data, stakeholder='integratesmanager@gmail.com'):
    """Get result."""
    request = await create_dummy_session(stakeholder)
    request.loaders = {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'project': ProjectLoader(),
        'single_vulnerability': SingleVulnerabilityLoader(),
        'vulnerability': VulnerabilityLoader()
    }
    _, result = await graphql(SCHEMA, data, context_value=request)
    return result
