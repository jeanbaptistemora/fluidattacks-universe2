from model.graph_model import (
    GraphShardMetadataLanguage,
)
from sast_syntax_readers.dispatchers.c_sharp import (
    CSHARP_DISPATCHERS,
)
from sast_syntax_readers.dispatchers.java import (
    JAVA_DISPATCHERS,
)
from sast_syntax_readers.dispatchers.javascript import (
    JAVASCRIPT_DISPATCHERS,
)
from sast_syntax_readers.types import (
    Dispatchers,
)
from typing import (
    Dict,
)

DISPATCHERS_BY_LANG: Dict[GraphShardMetadataLanguage, Dispatchers] = {
    GraphShardMetadataLanguage.CSHARP: CSHARP_DISPATCHERS,
    GraphShardMetadataLanguage.JAVA: JAVA_DISPATCHERS,
    GraphShardMetadataLanguage.JAVASCRIPT: JAVASCRIPT_DISPATCHERS,
}
