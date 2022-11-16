# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
)


class OrganizationIntegrationRepository(NamedTuple):
    id: str
    organization_id: str
    branch: str
    last_commit_date: str
    url: str
