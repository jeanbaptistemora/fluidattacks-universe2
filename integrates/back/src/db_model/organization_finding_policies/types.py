# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
)


class OrgFindingPolicyState(NamedTuple):
    modified_by: str
    modified_date: str
    status: str


class OrgFindingPolicy(NamedTuple):
    id: str
    name: str
    organization_name: str
    state: OrgFindingPolicyState
    tags: set[str]


class OrgFindingPolicyRequest(NamedTuple):
    organization_name: str
    policy_id: str
