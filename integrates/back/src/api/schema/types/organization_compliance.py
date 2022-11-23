from api.resolvers.organization_compliance import (
    standards,
)
from ariadne import (
    ObjectType,
)

ORGANIZATION_COMPLIANCE: ObjectType = ObjectType("OrganizationCompliance")
ORGANIZATION_COMPLIANCE.set_field("standards", standards.resolve)
