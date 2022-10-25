# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class CodeLanguagesTableRow:
    # pylint: disable=invalid-name
    id: str
    language: str
    loc: int
    root_id: str


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name
    id: str
    created_date: str
    group_name: str
    organization_name: str
    type: str
