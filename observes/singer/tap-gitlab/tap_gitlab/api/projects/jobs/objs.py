# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)


@dataclass(frozen=True)
class JobId:
    proj: ProjectId
    item_id: str

    def __str__(self) -> str:
        return f"JobId({self.proj.proj_id}, {self.item_id})"
