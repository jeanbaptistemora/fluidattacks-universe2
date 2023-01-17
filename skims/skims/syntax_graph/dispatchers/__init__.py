from model.graph_model import (
    GraphShardMetadataLanguage as GraphLanguage,
)
from syntax_graph.dispatchers.c_sharp import (
    CSHARP_DISPATCHERS,
)
from syntax_graph.dispatchers.dart import (
    DART_DISPATCHERS,
)
from syntax_graph.dispatchers.go import (
    GO_DISPATCHERS,
)
from syntax_graph.dispatchers.hcl import (
    HCL_DISPATCHERS,
)
from syntax_graph.dispatchers.java import (
    JAVA_DISPATCHERS,
)
from syntax_graph.dispatchers.javascript import (
    JAVASCRIPT_DISPATCHERS,
)
from syntax_graph.dispatchers.json import (
    JSON_DISPATCHERS,
)
from syntax_graph.dispatchers.kotlin import (
    KOTLIN_DISPATCHERS,
)
from syntax_graph.dispatchers.typescript import (
    TYPESCRIPT_DISPATCHERS,
)
from syntax_graph.dispatchers.yaml import (
    YAML_DISPATCHERS,
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
    GraphLanguage.GO: GO_DISPATCHERS,
    GraphLanguage.HCL: HCL_DISPATCHERS,
    GraphLanguage.JAVA: JAVA_DISPATCHERS,
    GraphLanguage.JAVASCRIPT: JAVASCRIPT_DISPATCHERS,
    GraphLanguage.JSON: JSON_DISPATCHERS,
    GraphLanguage.KOTLIN: KOTLIN_DISPATCHERS,
    GraphLanguage.TYPESCRIPT: TYPESCRIPT_DISPATCHERS,
    GraphLanguage.YAML: YAML_DISPATCHERS,
}
