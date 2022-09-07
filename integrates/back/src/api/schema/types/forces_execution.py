# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# None


from api.resolvers.forces_execution import (
    grace_period,
    log,
    severity_threshold,
    vulnerabilities,
)
from ariadne import (
    ObjectType,
)

FORCES_EXECUTION = ObjectType("ForcesExecution")
FORCES_EXECUTION.set_field("gracePeriod", grace_period.resolve)
FORCES_EXECUTION.set_field("log", log.resolve)
FORCES_EXECUTION.set_field("severityThreshold", severity_threshold.resolve)
FORCES_EXECUTION.set_field("vulnerabilities", vulnerabilities.resolve)
FORCES_EXECUTION.set_alias("executionId", "execution_id")
