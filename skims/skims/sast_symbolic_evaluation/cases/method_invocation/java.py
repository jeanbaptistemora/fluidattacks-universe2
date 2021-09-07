from model import (
    core_model,
)
from model.graph_model import (
    SyntaxStep,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    LookedUpClass,
)
from sast_symbolic_evaluation.utils_generic import (
    lookup_var_dcl_by_name,
    lookup_var_state_by_name,
)
from typing import (
    Set,
)
from utils.string import (
    build_attr_paths,
    split_on_first_dot,
)

WEAK_CIPHERS: Set[str] = {
    "md5",
    "sha1",
}


def attempt_java_util_properties_methods(args: EvaluatorArgs) -> bool:
    method_var, method_path = split_on_first_dot(args.syntax_step.method)

    if (
        dcl := lookup_var_dcl_by_name(args, method_var)
        # pylint: disable=used-before-assignment
    ) and dcl.var_type in build_attr_paths("java", "util", "Properties"):
        if method_path == "load" and len(args.dependencies) == 1:
            dcl.meta.value = args.dependencies[0].meta.value
        if (
            method_path == "getProperty"
            and len(args.dependencies) == 2
            and dcl.meta.value
        ):
            args.syntax_step.meta.value = dcl.meta.value.get(
                args.dependencies[-1].meta.value,
                args.dependencies[-2].meta.value,
            )
        return True

    return False


def attempt_java_security_msgdigest(args: EvaluatorArgs) -> bool:
    if (
        args.finding == core_model.FindingEnum.F052
        and args.syntax_step.method
        in {
            "java.security.MessageDigest.getInstance",
        }
        and len(args.dependencies) >= 1
        and isinstance(args.dependencies[-1].meta.value, str)
    ):
        args.syntax_step.meta.danger = (
            args.dependencies[-1].meta.value.lower() in WEAK_CIPHERS
        )
        return True

    return False


def attempt_java_looked_up_class(args: EvaluatorArgs) -> bool:
    method_var, method_path = split_on_first_dot(args.syntax_step.method)

    if (prnt := lookup_var_state_by_name(args, method_var)) and isinstance(
        # pylint: disable=used-before-assignment
        prnt.meta.value,
        LookedUpClass,
    ):
        method_path = f".{method_path}"

        if (method_path in prnt.meta.value.metadata.methods) and (
            return_step := args.eval_method(
                args,
                prnt.meta.value.metadata.methods[method_path].n_id,
                args.dependencies,
                args.graph_db.shards_by_path_f(prnt.meta.value.shard_path),
            )
        ):
            args.syntax_step.meta.danger = return_step.meta.danger
            args.syntax_step.meta.value = return_step.meta.value
            return True

    return False


def list_add(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    dcl.meta.value.append(args.dependencies[0])


def list_remove(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    index = int(args.dependencies[0].meta.value)
    dcl.meta.value.pop(index)
