from ariadne import graphql

from backend.api.dataloaders.event import EventLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader
from backend.api.dataloaders.group import GroupLoader
from backend.api.dataloaders.group_drafts import GroupDraftsLoader
from backend.api.dataloaders.group_findings import GroupFindingsLoader
from backend.api.dataloaders.group_roots import GroupRootsLoader
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from backend.api.schema import SCHEMA
from backend.domain import(
    project as group_domain,
)
from backend.utils import (
    user as user_utils,
)
from test_async.utils import create_dummy_session


async def complete_register(
    email: str,
    group_name: str,
):
    project_access = await group_domain.get_user_access(email, group_name)
    success = await user_utils.complete_register_for_group_invitation(
        project_access
    )

    return success


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
        'group_roots': GroupRootsLoader(),
        'vulnerability': VulnerabilityLoader()
    }
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result
