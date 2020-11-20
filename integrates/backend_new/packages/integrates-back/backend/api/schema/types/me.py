# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.me import (
    access_token,
    groups,
    organizations,
    permissions,
    remember,
    role,
    subscriptions_to_entity_report,
    tags
)


ME = ObjectType('Me')

ME.set_field('accessToken', access_token.resolve)
ME.set_field('permissions', permissions.resolve)
ME.set_field('projects', groups.resolve)
ME.set_field('organizations', organizations.resolve)
ME.set_field('remember', remember.resolve)
ME.set_field('role', role.resolve)
ME.set_field(
    'subscriptionsToEntityReport',
    subscriptions_to_entity_report.resolve
)
ME.set_field('tags', tags.resolve)
