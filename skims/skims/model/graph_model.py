# Standard library
from enum import (
    Enum,
)
from typing import (
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from model import (
    core_model,
)


class Graph(nx.DiGraph):
    pass


class GraphShardMetadataJavaClassMethod(NamedTuple):
    n_id: str


class GraphShardMetadataJavaClass(NamedTuple):
    methods: Dict[str, GraphShardMetadataJavaClassMethod]
    n_id: str


class GraphShardMetadataJava(NamedTuple):
    classes: Dict[str, GraphShardMetadataJavaClass]
    package: str


class GraphShardMetadataLanguage(Enum):
    JAVA: str = 'java'
    NOT_SUPPORTED: str = 'not_supported'


class GraphShardMetadata(NamedTuple):
    java: Optional[GraphShardMetadataJava]
    language: GraphShardMetadataLanguage


class GraphShardCacheable(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata


class GraphShard(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    path: str


class GraphDB(NamedTuple):
    shards: List[GraphShard]
    shards_by_path: Dict[str, int]


Query = Callable[[Graph], core_model.Vulnerabilities]
Queries = Tuple[Query, ...]
