# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)
from fa_purity.frozen import (
    FrozenDict,
)


class TargetTables(Enum):
    PROJ_COMMENTS = "fi_project_comments"
    FIN_COMMENTS = "fi_finding_comments"
    FORCES = "FI_forces"
    ACCESS = "FI_project_access"
    PROJECTS = "FI_projects"
    USERS = "FI_users"
    AUTHZ = "fi_authz"
    ORGANIZATIONS = "fi_organizations"
    EVENTS = "fi_events"
    CORE = "integrates_vms"


_tt = TargetTables
SEGMENTATION: FrozenDict[TargetTables, int] = FrozenDict(
    {
        _tt.PROJ_COMMENTS: 1,
        _tt.FIN_COMMENTS: 8,
        _tt.FORCES: 11,
        _tt.ACCESS: 2,
        _tt.PROJECTS: 1,
        _tt.USERS: 1,
        _tt.AUTHZ: 2,
        _tt.ORGANIZATIONS: 1,
        _tt.EVENTS: 1,
        _tt.CORE: 100,
    }
)
