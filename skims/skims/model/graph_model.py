# Future
from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from model import (
    core_model,
)
import networkx as nx
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)

NAttrs = Dict[str, str]
NAttrsPredicateFunction = Callable[[NAttrs], bool]
NId = str
NIdPredicateFunction = Callable[[str], bool]

SyntaxStep = Any
SyntaxSteps = List[SyntaxStep]
SyntaxStepsLazy = Iterator[SyntaxStep]


class CurrentInstance(NamedTuple):
    fields: Optional[Dict[str, Any]] = None


@dataclass
class SyntaxStepMeta:
    danger: bool
    dependencies: Any
    n_id: NId
    value: Optional[Any]

    @staticmethod
    def default(
        n_id: NId,
        dependencies: Optional[List[SyntaxSteps]] = None,
    ) -> SyntaxStepMeta:
        return SyntaxStepMeta(
            danger=False,
            dependencies=dependencies or [],
            n_id=n_id,
            value=None,
        )

    def linear(self) -> bool:
        return isinstance(self.dependencies, int)


class SyntaxStepAssignment(NamedTuple):
    meta: SyntaxStepMeta
    var: str

    type: str = "SyntaxStepAssignment"


class SyntaxStepBinaryExpression(NamedTuple):
    operator: str
    meta: SyntaxStepMeta

    type: str = "SyntaxStepBinaryExpression"


class SyntaxStepUnaryExpression(NamedTuple):
    meta: SyntaxStepMeta

    operator: str
    type: str = "SyntaxStepUnaryExpression"


class SyntaxStepDeclaration(NamedTuple):
    meta: SyntaxStepMeta
    var: str
    var_type: str
    modifiers: Optional[Set[str]] = None

    type: str = "SyntaxStepDeclaration"

    @property
    def var_type_base(self) -> str:
        portions = self.var_type.rsplit("[", maxsplit=1)
        return portions[0]


class SyntaxStepIf(NamedTuple):
    meta: SyntaxStepMeta
    n_id_false: Optional[NId]
    n_id_true: Optional[NId]

    type: str = "SyntaxStepIf"


class SyntaxStepSwitch(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepSwitch"


class SyntaxStepSwitchLabelCase(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepSwitchLabelCase"


class SyntaxStepSwitchLabelDefault(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepSwitchLabelDefault"


class SyntaxStepParenthesizedExpression(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepParenthesizedExpression"


class SyntaxStepCastExpression(NamedTuple):
    meta: SyntaxStepMeta
    cast_type: str

    type: str = "SyntaxStepCastExpression"


class SyntaxStepInstanceofExpression(NamedTuple):
    meta: SyntaxStepMeta
    instanceof_type: str

    type: str = "SyntaxStepInstanceofExpression"


class SyntaxStepCatchClause(NamedTuple):
    meta: SyntaxStepMeta

    catch_type: str
    var: str

    type: str = "SyntaxStepParenthesizedExpression"


class SyntaxStepFor(NamedTuple):
    meta: SyntaxStepMeta
    n_id_update: NId
    n_id_var_declaration: NId
    n_id_conditional_expression: NId

    type: str = "SyntaxStepFor"


class SyntaxStepLiteral(NamedTuple):
    meta: SyntaxStepMeta
    value: str
    value_type: str

    type: str = "SyntaxStepLiteral"


class SyntaxStepMethodInvocation(NamedTuple):
    meta: SyntaxStepMeta
    method: str
    current_instance: Optional[CurrentInstance] = None

    type: str = "SyntaxStepMethodInvocation"


class SyntaxStepLambdaExpression(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepLambdaExpression"


class SyntaxStepMethodInvocationChain(NamedTuple):
    meta: SyntaxStepMeta
    method: str
    current_instance: Optional[CurrentInstance] = None

    type: str = "SyntaxStepMethodInvocationChain"


class SyntaxStepNoOp(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepNoOp"


class SyntaxStepObjectInstantiation(NamedTuple):
    meta: SyntaxStepMeta
    object_type: str

    type: str = "SyntaxStepObjectInstantiation"


class SyntaxStepArrayInitialization(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepArrayInitialization"


class SyntaxStepArrayInstantiation(NamedTuple):
    meta: SyntaxStepMeta
    array_type: str

    type: str = "SyntaxStepArrayInstantiation"


class SyntaxStepReturn(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepReturn"


class SyntaxStepSymbolLookup(NamedTuple):
    meta: SyntaxStepMeta
    symbol: str

    type: str = "SyntaxStepSymbolLookup"


class SyntaxStepTernary(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepTernary"


class SyntaxStepThis(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepThis"


class SyntaxStepArrayAccess(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepArrayAccess"


class SyntaxStepMemberAccessExpression(NamedTuple):
    meta: SyntaxStepMeta
    member: str

    type: str = "SyntaxStepMemberAccessExpression"


class Graph(nx.DiGraph):
    pass


GraphSyntax = Dict[NId, SyntaxSteps]


class GraphShardMetadataClassField(NamedTuple):
    n_id: NId
    var: str
    var_type: str
    static: bool = False


class GraphShardMetadataParameter(NamedTuple):
    n_id: NId
    name: str
    type_name: str


class GraphShardMetadataCSharpParameter(NamedTuple):
    n_id: NId
    name: str
    type_name: str
    attributes: Optional[List[str]] = None


class GraphShardMetadataClassMethod(NamedTuple):
    n_id: NId
    class_name: Optional[str] = None
    name: Optional[str] = None
    parameters: Optional[Dict[str, GraphShardMetadataParameter]] = None
    return_type: Optional[str] = None
    static: bool = False


class GraphShardMetadataCSharpMethod(NamedTuple):
    n_id: NId
    class_name: Optional[str] = None
    parameters: Optional[Dict[str, GraphShardMetadataCSharpParameter]] = None
    name: Optional[str] = None
    return_type: Optional[str] = None
    static: bool = False
    attributes: Optional[List[str]] = None


class GraphShardMetadataClass(NamedTuple):
    fields: Dict[str, GraphShardMetadataClassField]
    methods: Dict[str, GraphShardMetadataClassMethod]
    n_id: NId
    inherit: Optional[Set[str]] = None


class GraphShardMetadataJava(NamedTuple):
    classes: Dict[str, GraphShardMetadataClass]
    package: str


class GraphShardMetadataCSharp(NamedTuple):
    classes: Dict[str, GraphShardMetadataClass]
    package: str


class GraphShardMetadataLanguage(Enum):
    CSHARP: str = "c_sharp"
    GO: str = "go"
    JAVA: str = "java"
    NOT_SUPPORTED: str = "not_supported"
    TSX: str = "tsx"


class GraphShardMetadata(NamedTuple):
    language: GraphShardMetadataLanguage
    java: Optional[GraphShardMetadataJava] = GraphShardMetadataJava(
        classes={},
        package="",
    )
    c_sharp: Optional[GraphShardMetadataCSharp] = GraphShardMetadataCSharp(
        classes={},
        package="",
    )


class GraphShardCacheable(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    syntax: GraphSyntax


class GraphShard(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    path: str
    syntax: GraphSyntax


class GraphVulnerabilityParameters(NamedTuple):
    cwe: Tuple[int, ...]
    desc_key: str
    desc_params: Dict[str, str]


GRAPH_VULNERABILITY_PARAMETERS: Dict[
    core_model.FindingEnum,
    GraphVulnerabilityParameters,
] = {
    core_model.FindingEnum.F001_C_SHARP_SQL: (
        GraphVulnerabilityParameters(
            cwe=(89,),
            desc_key="src.lib_path.F001_C_SHARP_SQL.user_controled_param",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F001_JAVA_SQL: (
        GraphVulnerabilityParameters(
            cwe=(89,),
            desc_key="src.lib_path.F001_JAVA_SQL.user_controled_param",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F004: GraphVulnerabilityParameters(
        cwe=(78,),
        desc_key="F004.description",
        desc_params={},
    ),
    core_model.FindingEnum.F008: GraphVulnerabilityParameters(
        cwe=(79,),
        desc_key="F008.description",
        desc_params={},
    ),
    core_model.FindingEnum.F021: GraphVulnerabilityParameters(
        cwe=(643,),
        desc_key="F021.description",
        desc_params={},
    ),
    core_model.FindingEnum.F034: GraphVulnerabilityParameters(
        cwe=(330,),
        desc_key="F034.description",
        desc_params={},
    ),
    core_model.FindingEnum.F042: GraphVulnerabilityParameters(
        cwe=(614,),
        desc_key="F042.description",
        desc_params={},
    ),
    core_model.FindingEnum.F052: GraphVulnerabilityParameters(
        cwe=(328,),
        desc_key="F052.description",
        desc_params={},
    ),
    core_model.FindingEnum.F063_PATH_TRAVERSAL: (
        GraphVulnerabilityParameters(
            cwe=(22,),
            desc_key="src.lib_path.f063_path_traversal.description",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F063_TRUSTBOUND: (
        GraphVulnerabilityParameters(
            cwe=(501,),
            desc_key="F063_TRUSTBOUND.description",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F107: (
        GraphVulnerabilityParameters(
            cwe=(90,),
            desc_key="F107.description",
            desc_params={},
        )
    ),
}


class GraphDBContext(NamedTuple):
    java_resources: Dict[str, Dict[str, str]]


class GraphDB(NamedTuple):
    context: GraphDBContext
    shards: List[GraphShard]
    shards_by_language_class: Dict[str, Dict[str, str]]
    shards_by_path: Dict[str, int]

    def shards_by_path_f(self, path: str) -> GraphShard:
        return self.shards[self.shards_by_path[path]]

    def shards_by_langauge(
        self,
        language: GraphShardMetadataLanguage,
    ) -> List[GraphShard]:
        return [
            shard
            for shard in self.shards
            if shard.metadata.language == language
        ]


GraphShardNode = Tuple[GraphShard, NId]
GraphShardNodes = Iterable[GraphShardNode]

Query = Callable[[Graph], core_model.Vulnerabilities]
Queries = Tuple[Tuple[core_model.FindingEnum, Query], ...]
