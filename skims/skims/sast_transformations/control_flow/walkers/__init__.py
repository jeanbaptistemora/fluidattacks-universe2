# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.types import (
    Walkers,
)
from sast_transformations.control_flow.walkers.c_sharp import (
    CSHARP_WALKERS,
)
from sast_transformations.control_flow.walkers.go import (
    GO_WALKERS,
)
from sast_transformations.control_flow.walkers.java import (
    JAVA_WALKERS,
)
from sast_transformations.control_flow.walkers.javascript import (
    JAVASCRIPT_WALKERS,
)
from sast_transformations.control_flow.walkers.kotlin import (
    KOTLIN_WALKERS,
)
from typing import (
    Dict,
)

WALKERS_BY_LANG: Dict[GraphShardMetadataLanguage, Walkers] = {
    GraphShardMetadataLanguage.CSHARP: CSHARP_WALKERS,
    GraphShardMetadataLanguage.GO: GO_WALKERS,
    GraphShardMetadataLanguage.JAVA: JAVA_WALKERS,
    GraphShardMetadataLanguage.JAVASCRIPT: JAVASCRIPT_WALKERS,
    GraphShardMetadataLanguage.KOTLIN: KOTLIN_WALKERS,
}
