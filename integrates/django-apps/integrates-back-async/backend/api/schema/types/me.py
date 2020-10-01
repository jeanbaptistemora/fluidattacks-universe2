# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.me import (
    access_token,
    groups,
    organizations,
    remember,
    role,
    subscriptions_to_entity_report
)


ME = ObjectType('Me')

ME.set_field('accessToken', access_token.resolve)
ME.set_field('projects', groups.resolve)
ME.set_field('organizations', organizations.resolve)
ME.set_field('remember', remember.resolve)
ME.set_field('role', role.resolve)
ME.set_field(
    'subscriptionsToEntityReport',
    subscriptions_to_entity_report.resolve
)
