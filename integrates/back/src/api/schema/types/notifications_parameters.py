# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# None


from api.resolvers.me import (
    notifications_parameters,
)
from ariadne import (
    ObjectType,
)

PREFERENCES = ObjectType("NotificationPreferences")

PREFERENCES.set_field("parameters", notifications_parameters.resolve)
