# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class CommentType(Enum):
    COMMENT: str = "COMMENT"
    CONSULT: str = "CONSULT"
    OBSERVATION: str = "OBSERVATION"
    VERIFICATION: str = "VERIFICATION"
    ZERO_RISK: str = "ZERO_RISK"
