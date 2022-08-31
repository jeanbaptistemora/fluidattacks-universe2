from api.resolvers.enrollment import (
    trial,
)
from ariadne import (
    ObjectType,
)

ENROLLMENT = ObjectType("Enrollment")
ENROLLMENT.set_field("trial", trial.resolve)
