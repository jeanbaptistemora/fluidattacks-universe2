from model.graph_model import (
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.types import (
    Walkers,
)
from sast_transformations.control_flow.walkers.c_sharp import (
    CSHARP_WALKERS,
)
from sast_transformations.control_flow.walkers.java import (
    JAVA_WALKERS,
)
from typing import (
    Dict,
)

WALKERS_BY_LANG: Dict[GraphShardMetadataLanguage, Walkers] = {
    GraphShardMetadataLanguage.CSHARP: CSHARP_WALKERS,
    GraphShardMetadataLanguage.JAVA: JAVA_WALKERS,
}
