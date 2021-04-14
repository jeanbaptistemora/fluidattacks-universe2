# Local libraries
from model import (
    core_model,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    JavaClassInstance,
)
from utils.string import (
    complete_attrs_on_set,
)


def evaluate(args: EvaluatorArgs) -> None:
    _syntax_step_declaration_danger(args)
    _syntax_step_declaration_values(args)


def _syntax_step_declaration_danger(args: EvaluatorArgs) -> None:
    # Analyze the arguments involved in the assignment
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    # Analyze if the binding itself is sensitive
    no_trust_findings = {
        core_model.FindingEnum.F001_JAVA_SQL,
        core_model.FindingEnum.F004,
        core_model.FindingEnum.F008,
        core_model.FindingEnum.F021,
        core_model.FindingEnum.F042,
        core_model.FindingEnum.F063_PATH_TRAVERSAL,
        core_model.FindingEnum.F063_TRUSTBOUND,
        core_model.FindingEnum.F107,
    }
    danger_types = {
        'javax.servlet.http.HttpServletRequest'
    }
    bind_danger = (
        args.finding in no_trust_findings
        and args.syntax_step.var_type in complete_attrs_on_set(danger_types)
    )

    # Local context
    args.syntax_step.meta.danger = bind_danger or args_danger


def _syntax_step_declaration_values(args: EvaluatorArgs) -> None:
    step = args.syntax_step
    if len(args.dependencies) == 1:
        declaration, = args.dependencies
        # The assignment object may not be of the declared type,
        # the declared type can be an interface or a generic type
        if isinstance(declaration.meta.value, JavaClassInstance):
            new_step = args.syntax_step._replace(
                var_type=declaration.meta.value.class_name)
            args.syntax_steps[args.syntax_step_index] = new_step
            step = new_step
        step.meta.value = args.dependencies[0].meta.value
