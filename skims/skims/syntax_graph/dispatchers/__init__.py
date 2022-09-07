# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphShardMetadataLanguage as GraphLanguage,
)
from syntax_graph.dispatchers.c_sharp import (
    CSHARP_DISPATCHERS,
)
from syntax_graph.dispatchers.dart import (
    DART_DISPATCHERS,
)
from syntax_graph.dispatchers.java import (
    JAVA_DISPATCHERS,
)
from syntax_graph.dispatchers.javascript import (
    JAVASCRIPT_DISPATCHERS,
)
from syntax_graph.types import (
    Dispatchers,
)
from typing import (
    Dict,
)

DISPATCHERS_BY_LANG: Dict[GraphLanguage, Dispatchers] = {
    GraphLanguage.CSHARP: CSHARP_DISPATCHERS,
    GraphLanguage.DART: DART_DISPATCHERS,
    GraphLanguage.JAVA: JAVA_DISPATCHERS,
    GraphLanguage.JAVASCRIPT: JAVASCRIPT_DISPATCHERS,
}
