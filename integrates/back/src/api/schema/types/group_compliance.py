from api.resolvers.group_compliance import (
    unfulfilled_standards,
)
from ariadne import (
    ObjectType,
)

GROUP_COMPLIANCE: ObjectType = ObjectType("GroupCompliance")
GROUP_COMPLIANCE.set_field(
    "unfulfilledStandards", unfulfilled_standards.resolve
)
