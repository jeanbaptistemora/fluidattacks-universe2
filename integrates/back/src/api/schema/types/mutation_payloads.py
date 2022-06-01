from api.resolvers.mutation_payload.update_toe_lines_payload import (
    toe_lines as update_toe_lines_payload_toe_lines,
)
from ariadne import (
    ObjectType,
)

UPDATETOELINESPAYLOAD = ObjectType("UpdateToeLinesPayload")
UPDATETOELINESPAYLOAD.set_field(
    "toeLines", update_toe_lines_payload_toe_lines.resolve
)
