# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.company import (
    trial,
)
from ariadne import (
    ObjectType,
)

COMPANY = ObjectType("Company")
COMPANY.set_field("trial", trial.resolve)
