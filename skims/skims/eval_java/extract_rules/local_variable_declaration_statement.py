# Third party libraries
import networkx as nx

# Local libraries
from eval_java.extract_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    StatementDeclaration,
)
from utils import (
    graph as g,
)


def extract(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    # localVariableDeclarationStatement = localVariableDeclaration ';'
    match = g.match_ast(graph, n_id, 'LocalVariableDeclaration')
    if c_id := match['LocalVariableDeclaration']:
        _local_variable_declaration(graph, c_id, ctx=ctx)
    else:
        common.not_implemented(extract, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)


def _local_variable_declaration(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    # variableModifier* unannType variableDeclaratorList
    # Mostly due to reducers this end up being:
    # - CustomUnannArrayType VariableDeclarator
    # - CustomUnannClassOrInterfaceType VariableDeclarator
    # - IdentifierRule VariableDeclarator
    c_ids = g.adj_ast(graph, n_id)

    if len(c_ids := g.adj_ast(graph, n_id)) == 2:
        var_attrs = graph.nodes[c_ids[1]]
        type_attrs = graph.nodes[c_ids[0]]

        if (
            type_attrs['label_type'] in {
                'CustomUnannArrayType',
                'CustomUnannClassOrInterfaceType',
                'IdentifierRule',
                'BOOLEAN',
                'BYTE',
                'CHAR',
                'DOUBLE',
                'FLOAT',
                'INT',
                'LONG'
            }
            # Binding
            and var_attrs['label_type'] == 'VariableDeclarator'
        ):
            _variable_declarator(
                graph,
                c_ids[1],
                ctx=ctx,
                type_attrs_label_text=graph.nodes[c_ids[0]]['label_text'],
            )
        elif (
            var_attrs['label_type'] == 'IdentifierRule'
            and type_attrs['label_type'] == 'IdentifierRule'
        ):
            # Add the variable to the mapping
            ctx.statements.append(StatementDeclaration(
                meta=get_default_statement_meta(),
                stack=[],
                var=var_attrs['label_text'],
                var_type=type_attrs['label_text'],
            ))
        else:
            common.not_implemented(_local_variable_declaration, n_id, ctx=ctx)
    else:
        common.not_implemented(_local_variable_declaration, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)


def _variable_declarator(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
    type_attrs_label_text: str,
) -> Context:
    ctx = common.ensure_context(ctx)

    # variableDeclaratorId ('=' variableInitializer)?
    match = g.match_ast(graph, n_id, 'IdentifierRule', 'ASSIGN', '__0__')

    if (
        (var_id := match['IdentifierRule'])
        and match['ASSIGN']
        and (src_id := match['__0__'])
    ):
        src_ctx = generic.extract(graph, src_id, ctx=None)
        common.merge_contexts(ctx, src_ctx)

        # Add the variable to the mapping
        ctx.statements.append(StatementDeclaration(
            meta=get_default_statement_meta(),
            stack=src_ctx.statements,
            var=graph.nodes[var_id]['label_text'],
            var_type=type_attrs_label_text,
        ))
    else:
        common.not_implemented(_local_variable_declaration, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
