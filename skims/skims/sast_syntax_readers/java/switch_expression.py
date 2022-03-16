from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepsLazy,
    SyntaxStepSwitch,
    SyntaxStepSwitchLabelCase,
    SyntaxStepSwitchLabelDefault,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    List,
    Union,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    switch_condition_id = node_attrs["label_field_condition"]
    switch_groups = g.adj_ast(args.graph, node_attrs["label_field_body"])[1:-1]

    label_syntax: List[
        Union[SyntaxStepSwitchLabelDefault, SyntaxStepSwitchLabelCase]
    ] = []
    for switch_group in switch_groups:
        switch_label_id = g.adj_ast(args.graph, switch_group)[0]
        case_statements = g.adj_ast(args.graph, switch_label_id)
        if len(case_statements) == 1:
            label_syntax.append(
                SyntaxStepSwitchLabelDefault(
                    meta=SyntaxStepMeta.default(switch_group)
                )
            )
        else:
            for statement in (
                node
                for node in case_statements[1:]
                if args.graph.nodes[node]["label_type"] != ","
            ):
                label_syntax.append(
                    SyntaxStepSwitchLabelCase(
                        meta=SyntaxStepMeta.default(
                            switch_group,
                            [
                                args.generic(args.fork_n_id(statement)),
                            ],
                        ),
                    )
                )
    yield SyntaxStepSwitch(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [label_syntax]
            + [
                args.generic(args.fork_n_id(switch_condition_id)),
            ],
        ),
    )
