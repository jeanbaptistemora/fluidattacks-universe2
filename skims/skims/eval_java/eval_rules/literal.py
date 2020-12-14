# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    common,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    StatementLiteral,
)

# Constants
LITERAL_TYPES_MAPPING = {
    'BooleanLiteral': 'bool',
    'CustomNumericLiteral': 'number',
    'IntegerLiteral': 'number',
    'NullLiteral': 'null',
    'StringLiteral': 'string',
}


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    n_attrs = graph.nodes[n_id]
    n_attrs_label_text = n_attrs['label_text']
    n_attrs_label_type = n_attrs['label_type']

    ctx.statements.append(StatementLiteral(
        meta=get_default_statement_meta(),
        value_type=LITERAL_TYPES_MAPPING.get(
            n_attrs_label_type,
            n_attrs_label_type,
        ),
        value=n_attrs_label_text,
    ))

    return common.mark_seen(ctx, n_id)
