from ariadne import graphql

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.dataloaders.single_vulnerability import (
    SingleVulnerabilityLoader
)
from backend.api.schema import SCHEMA
from backend.dal.helpers.redis import AREDIS_CLIENT
from backend.domain import user as user_domain
from test_async.utils import create_dummy_session


async def complete_all_user_access():
    prefix = 'fi_urltoken:'
    for urltoken in await AREDIS_CLIENT.keys(pattern=f'{prefix}*'):
        await user_domain.complete_user_register(urltoken[len(prefix):])


async def get_graphql_result(data, stakeholder, session_jwt=None):
    """Get graphql result."""
    request = await create_dummy_session(stakeholder, session_jwt)
    request.loaders = {
        'event': EventLoader(),
        'finding': FindingLoader(),
        'finding_vulns': FindingVulnsLoader(),
        'group': GroupLoader(),
        'group_drafts': GroupDraftsLoader(),
        'group_findings': GroupFindingsLoader(),
        'single_vulnerability': SingleVulnerabilityLoader(),
    }
    _, result = await graphql(SCHEMA, data, context_value=request)
    await complete_all_user_access()
    return result
