# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from typing import (
    Optional,
)


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name
    id: str
    cvss_version: Optional[str]
    group_name: str
    hacker_email: str
    requirements: str
    sorts: str
    title: str
