# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from db_model.groups.enums import (
    GroupManaged,
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
    Optional,
)


def filter_active_groups(groups: tuple[Group, ...]) -> tuple[Group, ...]:
    return tuple(
        group
        for group in groups
        if group.state.status == GroupStateStatus.ACTIVE
        and group.state.managed != GroupManaged.UNDER_REVIEW
    )


def filter_deleted_groups(groups: tuple[Group, ...]) -> tuple[Group, ...]:
    return tuple(
        group
        for group in groups
        if group.state.status == GroupStateStatus.DELETED
    )


async def get_group_max_acceptance_days(
    *, loaders: Any, group: Group
) -> Optional[int]:
    if group.policies:
        return group.policies.max_acceptance_days

    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    return organization.policies.max_acceptance_days


async def get_group_max_number_acceptances(
    *, loaders: Any, group: Group
) -> Optional[int]:
    if group.policies:
        return group.policies.max_number_acceptances

    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    return organization.policies.max_number_acceptances


async def get_group_max_acceptance_severity(
    *, loaders: Any, group: Group
) -> Decimal:
    if group.policies:
        return (
            group.policies.max_acceptance_severity
            if group.policies.max_acceptance_severity is not None
            else DEFAULT_MAX_SEVERITY
        )

    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    return (
        organization.policies.max_acceptance_severity
        if organization.policies.max_acceptance_severity is not None
        else DEFAULT_MAX_SEVERITY
    )


async def get_group_min_acceptance_severity(
    *, loaders: Any, group: Group
) -> Decimal:

    if group.policies:
        return group.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY

    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    return (
        organization.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY
    )
