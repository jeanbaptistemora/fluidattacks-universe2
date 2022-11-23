from api.resolvers.company import (
    trial,
)
from ariadne import (
    ObjectType,
)

COMPANY = ObjectType("Company")
COMPANY.set_field("trial", trial.resolve)
