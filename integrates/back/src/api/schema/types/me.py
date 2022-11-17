# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.me import (
    access_token,
    company,
    credentials,
    drafts,
    enrollment,
    finding_reattacks,
    has_drafts_rejected,
    is_concurrent_session,
    notifications_preferences,
    organizations,
    pending_events,
    permissions,
    phone,
    reattacks,
    remember,
    role,
    subscriptions_to_entity_report,
    tags,
    tours,
    vulnerabilities_assigned,
)
from ariadne import (
    ObjectType,
)

ME = ObjectType("Me")
ME.set_field("accessToken", access_token.resolve)
ME.set_field("company", company.resolve)
ME.set_field("credentials", credentials.resolve)
ME.set_field("drafts", drafts.resolve)
ME.set_field("enrollment", enrollment.resolve)
ME.set_field("findingReattacks", finding_reattacks.resolve)
ME.set_field("hasDraftsRejected", has_drafts_rejected.resolve)
ME.set_field("isConcurrentSession", is_concurrent_session.resolve)
ME.set_field("organizations", organizations.resolve)
ME.set_field("pendingEvents", pending_events.resolve)
ME.set_field("permissions", permissions.resolve)
ME.set_field("phone", phone.resolve)
ME.set_field("reattacks", reattacks.resolve)
ME.set_field("remember", remember.resolve)
ME.set_field("role", role.resolve)
ME.set_field(
    "subscriptionsToEntityReport", subscriptions_to_entity_report.resolve
)
ME.set_field("tags", tags.resolve)
ME.set_field("tours", tours.resolve)
ME.set_field("vulnerabilitiesAssigned", vulnerabilities_assigned.resolve)
ME.set_field("notificationsPreferences", notifications_preferences.resolve)
