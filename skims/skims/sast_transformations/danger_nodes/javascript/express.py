from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphSyntax,
    SyntaxStepDeclaration,
    SyntaxStepMethodInvocation,
    SyntaxStepMethodInvocationChain,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from sast_transformations.danger_nodes.utils import (
    _append_label_input,
)

FINDINGS = {
    FindingEnum.F001,
    FindingEnum.F004,
    FindingEnum.F008,
    FindingEnum.F021,
    FindingEnum.F063,
    FindingEnum.F107,
}


def mark_requests(
    graph: Graph,
    graph_syntax_steps: GraphSyntax,
) -> None:
    for syntax_steps in graph_syntax_steps.values():
        for index, syntax_step in enumerate(syntax_steps):
            if isinstance(
                syntax_step,
                (
                    SyntaxStepMethodInvocation,
                    SyntaxStepMethodInvocationChain,
                ),
            ):
                http_methods = {"get", "post", "put", "delete"}
                if not http_methods.intersection(
                    set(syntax_step.method.split("."))
                ):
                    continue
                methods_arguments = [
                    dependencies
                    for dependencies in get_dependencies(
                        syntax_step_index=index, syntax_steps=syntax_steps
                    )
                    if isinstance(dependencies, SyntaxStepDeclaration)
                ][:-1]
                for _parameter in methods_arguments:
                    for finding in FINDINGS:
                        _append_label_input(
                            graph, _parameter.meta.n_id, finding
                        )
