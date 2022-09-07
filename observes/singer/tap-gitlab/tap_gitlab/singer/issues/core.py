# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class SingerStreams(Enum):
    issue_assignees = "issue_assignees"
    issue_labels = "issue_labels"
    issue = "issue"
