# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.enrollment import (
    trial,
)
from ariadne import (
    ObjectType,
)

ENROLLMENT = ObjectType("Enrollment")
ENROLLMENT.set_field("trial", trial.resolve)
