# None


from api.resolvers.me import (
    access_token,
    has_mobile_app,
    is_concurrent_session,
    organizations,
    permissions,
    remember,
    role,
    subscriptions_to_entity_report,
    tags,
)
from ariadne import (
    ObjectType,
)

ME = ObjectType("Me")
ME.set_field("accessToken", access_token.resolve)
ME.set_field("hasMobileApp", has_mobile_app.resolve)
ME.set_field("isConcurrentSession", is_concurrent_session.resolve)
ME.set_field("organizations", organizations.resolve)
ME.set_field("permissions", permissions.resolve)
ME.set_field("remember", remember.resolve)
ME.set_field("role", role.resolve)
ME.set_field(
    "subscriptionsToEntityReport", subscriptions_to_entity_report.resolve
)
ME.set_field("tags", tags.resolve)
