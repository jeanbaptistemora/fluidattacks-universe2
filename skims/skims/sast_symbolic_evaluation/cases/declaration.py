from model import (
    core_model,
)
from model.graph_model import (
    GraphShardMetadataLanguage,
    SyntaxStepDeclaration,
    SyntaxStepMethodInvocation,
)
from sast_symbolic_evaluation.cases.method_invocation.javascript import (
    process_declaration as javascript_process_declaration,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    JavaClassInstance,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)


def evaluate(args: EvaluatorArgs) -> None:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVASCRIPT:
        javascript_process_declaration(args)
    _syntax_step_declaration_danger(args)
    _syntax_step_declaration_values(args)


def _syntax_step_declaration_danger(args: EvaluatorArgs) -> None:
    # Analyze the arguments involved in the assignment or the current danger
    # in case it was set in previous steps (when declaring a called function)
    args_danger = (
        any(dep.meta.danger for dep in args.dependencies)
        or args.syntax_step.meta.danger
    )

    # Analyze if the binding itself is sensitive
    no_trust_findings = {
        core_model.FindingEnum.F112,
        core_model.FindingEnum.F001,
        core_model.FindingEnum.F004,
        core_model.FindingEnum.F008,
        core_model.FindingEnum.F021,
        core_model.FindingEnum.F042,
        core_model.FindingEnum.F063,
        core_model.FindingEnum.F089,
        core_model.FindingEnum.F107,
    }
    danger_types = {
        "javax.servlet.http.HttpServletRequest",
        "System.Web.HttpRequest",
        "Request",
    }
    danger_modifiers = {
        "org.springframework.web.bind.annotation.RequestParam",
    }
    bind_danger = args.finding in no_trust_findings and (
        args.syntax_step.var_type in complete_attrs_on_set(danger_types)
        or (
            args.syntax_step.modifiers
            and bool(
                complete_attrs_on_set(danger_modifiers).intersection(
                    args.syntax_step.modifiers
                )
            )
        )
    )

    # Analyze if the case is a declaration of a previously called function
    prev_step = args.syntax_steps[args.syntax_step_index - 1]
    if (
        isinstance(prev_step, SyntaxStepMethodInvocation)
        and args.shard.graph.nodes[
            g.lookup_first_cfg_parent(
                args.shard.graph, args.syntax_step.meta.n_id
            )
        ]["label_type"]
        == "function_declaration"
    ):
        # Propagate danger from all the arguments of the called function to
        # the new declarations
        prev_step_deps = get_dependencies(
            args.syntax_step_index - 1, args.syntax_steps
        )
        for idx, dep in enumerate(reversed(prev_step_deps)):
            if not idx:
                args_danger = dep.meta.danger
            else:
                args.syntax_steps[
                    args.syntax_step_index + idx
                ].meta.danger = dep.meta.danger

    args.syntax_step.meta.danger = bind_danger or args_danger


def _syntax_step_declaration_values(args: EvaluatorArgs) -> None:
    step: SyntaxStepDeclaration = args.syntax_step
    if len(args.dependencies) == 1:
        (declaration,) = args.dependencies
        # The assignment object may not be of the declared type,
        # the declared type can be an interface or a generic type
        if (
            isinstance(declaration.meta.value, JavaClassInstance)
            and not step.var_type
        ):
            step.var_type = declaration.meta.value.class_name
        step.meta.value = args.dependencies[0].meta.value
    elif args.dependencies:
        step.meta.value = args.dependencies[-1].meta.value

    # Analyze if the case is a declaration of a previously called function
    prev_step = args.syntax_steps[args.syntax_step_index - 1]

    if (
        isinstance(prev_step, SyntaxStepMethodInvocation)
        and args.shard.graph.nodes[
            g.lookup_first_cfg_parent(
                args.shard.graph, args.syntax_step.meta.n_id
            )
        ]["label_type"]
        == "function_declaration"
    ):
        # Propagate value from all the arguments of the called function to
        # the new declarations
        prev_step_deps = get_dependencies(
            args.syntax_step_index - 1, args.syntax_steps
        )
        for idx, dep in enumerate(reversed(prev_step_deps)):
            args.syntax_steps[
                args.syntax_step_index + idx
            ].meta.value = dep.meta.value
