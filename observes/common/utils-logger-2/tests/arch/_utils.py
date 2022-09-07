# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Any,
    Callable,
)


def map_over_children(
    graph: Any, module: str, function: Callable[[str, str], None]
) -> None:
    children = frozenset(graph.find_children(module))
    for c in children:
        function(module, c)
        map_over_children(graph, c, function)
