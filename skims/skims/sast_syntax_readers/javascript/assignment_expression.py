from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
    Union,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    assignments = tuple(_expression(args, args.n_id))
    last_assignment = assignments[-1]
    for var_identifier in assignments[:-1]:
        yield graph_model.SyntaxStepAssignment(
            meta=last_assignment.meta,  # type: ignore
            var=var_identifier,
        )
    yield last_assignment


def _expression(
    args: SyntaxReaderArgs, expression_id: str
) -> Iterator[Union[str, graph_model.SyntaxStepAssignment]]:
    node_attributes = args.graph.nodes[expression_id]

    left_id = node_attributes["label_field_left"]
    src_id = node_attributes["label_field_right"]

    left_type = args.graph.nodes[left_id]["label_type"]
    if left_type == "identifier":
        identifier_name = args.graph.nodes[left_id]["label_text"]
    elif left_type == "member_expression":
        identifier_name = node_to_str(args.graph, left_id)
    elif left_type == "subscript_expression":
        subscript_attrs = args.graph.nodes[left_id]
        _object_attrs = args.graph.nodes[subscript_attrs["label_field_object"]]
        _index_attrs = args.graph.nodes[subscript_attrs["label_field_index"]]
        if (object_name := _object_attrs.get("label_text")) and (
            index_text := _index_attrs.get("label_text")
        ):
            index_text = index_text.replace('"', "").replace("'", "")
            identifier_name = f"{object_name}.{index_text}"
    else:
        raise MissingCaseHandling(args)

    if args.graph.nodes[src_id]["label_type"] == "assignment_expression":
        yield identifier_name
        yield from _expression(args, src_id)
    else:
        yield graph_model.SyntaxStepAssignment(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(src_id)),
                ],
            ),
            var=identifier_name,
        )
