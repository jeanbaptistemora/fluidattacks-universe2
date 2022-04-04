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
    Union,
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


class SyntaxStepAttributeAccess(NamedTuple):
    attribute: str
    meta: SyntaxStepMeta

    type: str = "SyntaxStepAttributeAccess"


class SyntaxStepAssignment(NamedTuple):
    meta: SyntaxStepMeta
    var: str
    attribute: str = ""

    type: str = "SyntaxStepAssignment"


class SyntaxStepBinaryExpression(NamedTuple):
    operator: str
    meta: SyntaxStepMeta

    type: str = "SyntaxStepBinaryExpression"


class SyntaxStepUnaryExpression(NamedTuple):
    meta: SyntaxStepMeta

    operator: str
    type: str = "SyntaxStepUnaryExpression"


@dataclass
class SyntaxStepDeclaration:
    meta: SyntaxStepMeta
    var: str
    var_type: Optional[str] = None
    modifiers: Optional[Set[str]] = None
    is_destructuring: bool = False

    type: str = "SyntaxStepDeclaration"

    @property
    def var_type_base(self) -> Optional[str]:
        if self.var_type:
            portions = self.var_type.rsplit("[", maxsplit=1)
            return portions[0]
        return None


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

    var: str
    catch_type: Optional[str] = None

    type: str = "SyntaxStepCatchClause"


class SyntaxStepLoop(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepLoop"


class SyntaxStepLiteral(NamedTuple):
    meta: SyntaxStepMeta
    value: Union[str, Dict]
    value_type: str

    type: str = "SyntaxStepLiteral"


class SyntaxStepMethodDeclaration(NamedTuple):
    meta: SyntaxStepMeta
    name: str
    type: str = "SyntaxStepMethodDeclaration"


@dataclass
class SyntaxStepMethodInvocation:
    meta: SyntaxStepMeta
    method: str
    current_instance: Optional[CurrentInstance] = None
    return_type: Optional[str] = None

    type: str = "SyntaxStepMethodInvocation"


class SyntaxStepPrefixExpression(NamedTuple):
    prefix: str
    meta: SyntaxStepMeta

    type: str = "SyntaxStepPrefixExpression"


@dataclass
class SyntaxStepLambdaExpression:
    meta: SyntaxStepMeta

    lambda_type: Optional[str] = None
    type: str = "SyntaxStepLambdaExpression"


class SyntaxStepMethodInvocationChain(NamedTuple):
    meta: SyntaxStepMeta
    method: str
    expression: Optional[str] = None
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


class SyntaxStepSubscriptExpression(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepSubscriptExpression"


class SyntaxStepMemberAccessExpression(NamedTuple):
    meta: SyntaxStepMeta
    member: str
    expression: str

    type: str = "SyntaxStepMemberAccessExpression"


class SyntaxStepTemplateString(NamedTuple):
    meta: SyntaxStepMeta

    type: str = "SyntaxStepTemplateString"


class SyntaxStepNamedArgument(NamedTuple):
    meta: SyntaxStepMeta
    var: str

    type: str = "SyntaxStepNamedArgument"


class SyntaxStepDefaultParameter(NamedTuple):
    meta: SyntaxStepMeta
    var: str
    var_type: str

    type: str = "SyntaxStepDefaultParameter"


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
    attributes: Optional[List[str]] = None


class GraphShardMetadataClassMethod(NamedTuple):
    n_id: NId
    class_name: Optional[str] = None
    name: Optional[str] = None
    parameters: Optional[Dict[str, GraphShardMetadataParameter]] = None
    return_type: Optional[str] = None
    static: bool = False
    attributes: Optional[List[str]] = None


class GraphShardMetadataClass(NamedTuple):
    fields: Dict[str, GraphShardMetadataClassField]
    methods: Dict[str, GraphShardMetadataClassMethod]
    n_id: NId
    attributes: Optional[List[str]] = None
    inherit: Optional[Union[Set[str], str]] = None


class SinkFunctions(NamedTuple):
    name: str
    n_id: NId
    s_id: NId


class GraphShardMetadataJava(NamedTuple):
    classes: Dict[str, GraphShardMetadataClass]
    package: str


class GraphShardMetadataCSharp(NamedTuple):
    classes: Dict[str, GraphShardMetadataClass]
    package: str


class GraphShardMetadataGo(NamedTuple):
    imports: List[str]
    sink_functions: Dict[str, List[SinkFunctions]]
    package: str


class GraphShardMetadataLanguage(Enum):
    CSHARP: str = "c_sharp"
    GO: str = "go"
    JAVA: str = "java"
    JAVASCRIPT: str = "javascript"
    KOTLIN: str = "kotlin"
    NOT_SUPPORTED: str = "not_supported"
    PHP: str = "php"
    RUBY: str = "ruby"
    SCALA: str = "scala"
    TSX: str = "tsx"


class GraphShardMetadata(NamedTuple):
    language: GraphShardMetadataLanguage
    c_sharp: Optional[GraphShardMetadataCSharp] = GraphShardMetadataCSharp(
        classes={},
        package="",
    )
    go: Optional[GraphShardMetadataGo] = GraphShardMetadataGo(
        imports=[],
        sink_functions={},
        package="",
    )
    java: Optional[GraphShardMetadataJava] = GraphShardMetadataJava(
        classes={},
        package="",
    )


class GraphShardCacheable(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    syntax: GraphSyntax
    syntax_graph: Optional[Graph]


class GraphShard(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    path: str
    syntax: GraphSyntax
    syntax_graph: Optional[Graph]


class GraphVulnerabilityParameters(NamedTuple):
    desc_key: str
    desc_params: Dict[str, str]


GRAPH_VULNERABILITY_PARAMETERS: Dict[
    core_model.FindingEnum,
    GraphVulnerabilityParameters,
] = {
    core_model.FindingEnum.F001: (
        GraphVulnerabilityParameters(
            desc_key="src.lib_path.F001.user_controled_param",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F112: (
        GraphVulnerabilityParameters(
            desc_key="src.lib_path.F112.user_controled_param",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F004: GraphVulnerabilityParameters(
        desc_key="criteria.vulns.004.description",
        desc_params={},
    ),
    core_model.FindingEnum.F008: GraphVulnerabilityParameters(
        desc_key="criteria.vulns.008.description",
        desc_params={},
    ),
    core_model.FindingEnum.F021: GraphVulnerabilityParameters(
        desc_key="criteria.vulns.021.description",
        desc_params={},
    ),
    core_model.FindingEnum.F034: GraphVulnerabilityParameters(
        desc_key="criteria.vulns.034.description",
        desc_params={},
    ),
    core_model.FindingEnum.F035: GraphVulnerabilityParameters(
        desc_key="criteria.vulns.035.description",
        desc_params={},
    ),
    core_model.FindingEnum.F042: GraphVulnerabilityParameters(
        desc_key="criteria.vulns.042.description",
        desc_params={},
    ),
    core_model.FindingEnum.F052: GraphVulnerabilityParameters(
        desc_key="criteria.vulns.052.description",
        desc_params={},
    ),
    core_model.FindingEnum.F063: (
        GraphVulnerabilityParameters(
            desc_key="src.lib_path.f063_path_traversal.description",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F089: (
        GraphVulnerabilityParameters(
            desc_key="criteria.vulns.089.description",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F100: (
        GraphVulnerabilityParameters(
            desc_key="criteria.vulns.100.description",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F127: (
        GraphVulnerabilityParameters(
            desc_key=(core_model.FindingEnum.F127.value.description),
            desc_params={},
        )
    ),
    core_model.FindingEnum.F107: (
        GraphVulnerabilityParameters(
            desc_key="criteria.vulns.107.description",
            desc_params={},
        )
    ),
    core_model.FindingEnum.F320: (
        GraphVulnerabilityParameters(
            desc_key="criteria.vulns.320.description",
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

    def shards_by_language(
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

Query = Union[
    Callable[[Graph], core_model.Vulnerabilities],
    Callable[[Any, GraphDB], core_model.Vulnerabilities],
]
Queries = Tuple[Tuple[core_model.FindingEnum, Query], ...]
