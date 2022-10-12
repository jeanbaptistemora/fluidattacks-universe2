# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._checks.encoders import (
    encoder as check_encoder,
)
from ._encoder import (
    ObjEncoder,
)
from tap_checkly.api2.checks import (
    CheckObj,
)

checks: ObjEncoder[CheckObj] = check_encoder
