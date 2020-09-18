# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    require_login,
    require_organization_access
)
from backend.domain import organization as org_domain
from backend.typing import Organization


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _obj: None,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> Organization:
    org_id: str = kwargs.get('organization_id', '')
    name: str = kwargs.get('organization_name', '')

    organization: Organization = (
        await org_domain.get_by_id(org_id)
        if org_id
        else await org_domain.get_by_name(name)
    )

    return {
        'id': organization['id'],
        'max_acceptance_days': organization['max_acceptance_days'],
        'max_acceptance_severity': organization['max_acceptance_severity'],
        'max_number_acceptations': organization['max_number_acceptations'],
        'min_acceptance_severity': organization['min_acceptance_severity'],
        'name': organization['name']
    }
