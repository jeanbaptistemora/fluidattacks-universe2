from ariadne import graphql

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.single_vulnerability import (
    SingleVulnerabilityLoader
)
from backend.api.dataloaders.project import ProjectLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from backend.dal.helpers.redis import AREDIS_CLIENT
from backend.domain import user as user_domain
from test_async.utils import create_dummy_session


async def complete_all_user_access():
    prefix = 'fi_urltoken:'
    for urltoken in await AREDIS_CLIENT.keys(pattern=f'{prefix}*'):
        await user_domain.complete_user_register(urltoken[len(prefix):])


async def get_graphql_result(data, stakeholder):
    """Get graphql result."""
    request = await create_dummy_session(stakeholder)
    request.loaders = {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'group': GroupLoader(),
        'project': ProjectLoader(),
        'single_vulnerability': SingleVulnerabilityLoader(),
        'vulnerability': VulnerabilityLoader()
    }
    _, result = await graphql(SCHEMA, data, context_value=request)
    await complete_all_user_access()
    return result
