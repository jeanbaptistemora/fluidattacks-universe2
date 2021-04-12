# Local libraries
from model import (
    core_model,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    JavaClassInstance,
)
from sast_symbolic_evaluation.utils_java import (
    lookup_java_class,
    lookup_java_method,
)
from utils.string import (
    build_attr_paths,
    complete_attrs_on_set,
    split_on_last_dot,
)


def evaluate(args: EvaluatorArgs) -> None:
    _syntax_step_object_instantiation_danger(args)
    _syntax_step_object_instantiation_values(args)


def _syntax_step_object_instantiation_danger(args: EvaluatorArgs) -> None:
    # Analyze the arguments involved in the instantiation
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    _danger_instances_by_finding = {
        core_model.FindingEnum.F063_PATH_TRAVERSAL.name: {
            'java.io.File',
            'java.io.FileInputStream',
            'java.io.FileOutputStream',
        },
        core_model.FindingEnum.F004.name: {
            'java.lang.ProcessBuilder',
        }
    }
    _danger_instances_no_args_by_finding = {
        core_model.FindingEnum.F034.name: {
            'java.util.Random',
        }
    }
    _danger_instances = {
        'java.lang.StringBuilder',
        'org.owasp.benchmark.helpers.SeparateClassRequest',
    }

    danger_instances_by_finding = {
        find: complete_attrs_on_set(instances)
        for find, instances in _danger_instances_by_finding.items()
    }
    danger_instances_no_args_by_finding = {
        find: complete_attrs_on_set(instances)
        for find, instances in _danger_instances_no_args_by_finding.items()
    }
    danger_instances = complete_attrs_on_set(_danger_instances)

    # Analyze if the object being instantiated is dangerous
    object_type: str = args.syntax_step.object_type
    instantiation_danger = (
        object_type in danger_instances_by_finding.get(
            args.finding.name, set())
        or object_type in danger_instances
    )
    # Analyze instances of objects that are vulnerable and do not
    # require any parameters
    instantiation_danger_no_args = (
        object_type
        in danger_instances_no_args_by_finding.get(args.finding.name, set())
    )

    if instantiation_danger_no_args:
        args.syntax_step.meta.danger = True
    elif instantiation_danger:
        args.syntax_step.meta.danger = args_danger if args else True
    else:
        args.syntax_step.meta.danger = args_danger


def _syntax_step_object_instantiation_values(args: EvaluatorArgs) -> None:
    object_type: str = args.syntax_step.object_type

    if object_type in build_attr_paths('java', 'util', 'ArrayList'):
        args.syntax_step.meta.value = []
    elif object_type in build_attr_paths('java', 'util', 'HashMap'):
        args.syntax_step.meta.value = {}
    elif args.graph_db.shards_by_java_class.get(
            object_type) or args.graph_db.shards_by_java_class.get(
                f'.{object_type}'):
        if '.' not in object_type:
            object_type = '.' + object_type

        constructor_name = (
            f'{object_type}.{split_on_last_dot(object_type)[1]}'
            f'_{len(args.dependencies)}'
        )
        if _method := lookup_java_method(
            args,
            constructor_name,
            object_type,
        ):
            if args.shard.path != _method.shard_path and (
                fields_modified := args.eval_constructor(
                    args,
                    _method.metadata.n_id,
                    args.dependencies,
                    args.graph_db.shards_by_path_f(_method.shard_path),
                )
            ):
                args.syntax_step.meta.value = JavaClassInstance(
                    fields=fields_modified,
                )
    elif java_class := lookup_java_class(args, object_type):
        args.syntax_step.meta.value = java_class
