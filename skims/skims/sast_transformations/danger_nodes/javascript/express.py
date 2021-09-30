from contextlib import (
    suppress,
)
from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphSyntax,
    SyntaxStepDeclaration,
    SyntaxStepLambdaExpression,
    SyntaxStepMethodInvocation,
    SyntaxStepMethodInvocationChain,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies_with_index,
)
from sast_transformations.danger_nodes.utils import (
    append_label_input,
)

FINDINGS = {
    FindingEnum.F112,
    FindingEnum.F004,
    FindingEnum.F008,
    FindingEnum.F021,
    FindingEnum.F042,
    FindingEnum.F063,
    FindingEnum.F107,
}


def mark_requests(
    graph: Graph,
    graph_syntax_steps: GraphSyntax,
) -> None:
    for syntax_steps in graph_syntax_steps.values():
        for index, syntax_step in enumerate(syntax_steps):
            if not isinstance(
                syntax_step,
                (
                    SyntaxStepMethodInvocation,
                    SyntaxStepMethodInvocationChain,
                ),
            ):
                continue
            http_methods = {"get", "post", "put", "delete"}
            if not http_methods.intersection(
                set(syntax_step.method.split("."))
            ):
                continue
            for handler_index in [
                dependencies[0]
                for dependencies in get_dependencies_with_index(
                    syntax_step_index=index, syntax_steps=syntax_steps
                )
                if isinstance(dependencies[1], SyntaxStepLambdaExpression)
            ]:
                req: SyntaxStepDeclaration
                res: SyntaxStepDeclaration
                handler_arguments = get_dependencies_with_index(
                    syntax_step_index=handler_index,
                    syntax_steps=syntax_steps,
                )
                if len(handler_arguments) == 1:
                    # pylint: disable=unbalanced-tuple-unpacking
                    (req,) = handler_arguments
                elif len(handler_arguments) == 2:
                    # pylint: disable=unbalanced-tuple-unpacking
                    req, res = handler_arguments
                elif len(handler_arguments) == 3:
                    # pylint: disable=unbalanced-tuple-unpacking
                    req, res, _ = handler_arguments

                for finding in FINDINGS:
                    with suppress(AttributeError, TypeError):
                        append_label_input(graph, req[1].meta.n_id, finding)
                    with suppress(AttributeError, TypeError):
                        append_label_input(graph, res[1].meta.n_id, finding)

                # add the type to the parameters, the type is only known
                # at runtime
                req[1].var_type = "Request"
                res[1].var_type = "Response"
