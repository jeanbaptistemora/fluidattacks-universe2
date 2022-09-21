# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_graph.syntax_readers.common import (
    program as common_program,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

TSX_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=common_program.reader,
    ),
)
