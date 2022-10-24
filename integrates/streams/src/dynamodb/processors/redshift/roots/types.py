# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from typing import (
    Optional,
)


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name
    id: str
    created_date: str
    group_name: str
    organization_name: str
    type: str


@dataclass(frozen=True)
class RootCodeLanguagesTableRow:
    # pylint: disable=invalid-name
    id: str
    language: str
    loc: int


@dataclass(frozen=True)
class RootEnvironmentUrlTableRow:
    # pylint: disable=invalid-name
    id: str
    cloud_name: Optional[str]
    created_at: datetime
    root_id: str
    url_type: Optional[str]
