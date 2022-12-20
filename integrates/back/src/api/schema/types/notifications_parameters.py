from api.resolvers.me import (
    notifications_parameters,
)
from ariadne import (
    ObjectType,
)

PREFERENCES = ObjectType("NotificationPreferences")

PREFERENCES.set_field("parameters", notifications_parameters.resolve)
