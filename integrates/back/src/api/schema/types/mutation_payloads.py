# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.mutation_payload.update_toe_input_payload import (
    toe_input as update_toe_input_payload_toe_input,
)
from api.resolvers.mutation_payload.update_toe_lines_payload import (
    toe_lines as update_toe_lines_payload_toe_lines,
)
from ariadne import (
    ObjectType,
)

UPDATE_TOE_INPUT_PAYLOAD = ObjectType("UpdateToeInputPayload")
UPDATE_TOE_INPUT_PAYLOAD.set_field(
    "toeInput", update_toe_input_payload_toe_input.resolve
)

UPDATE_TOE_LINES_PAYLOAD = ObjectType("UpdateToeLinesPayload")
UPDATE_TOE_LINES_PAYLOAD.set_field(
    "toeLines", update_toe_lines_payload_toe_lines.resolve
)
