# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
)

# Constants
SNIPPETS_CONTEXT: int = 10
SNIPPETS_COLUMNS: int = 12 * SNIPPETS_CONTEXT


class SnippetViewport(NamedTuple):
    column: int
    line: int

    columns_per_line: int = SNIPPETS_COLUMNS
    line_context: int = SNIPPETS_CONTEXT
    wrap: bool = False
