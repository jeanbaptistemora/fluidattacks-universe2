# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    StatementCustomMethodInvocation,
    StatementCustomMethodInvocationChain,
)
from utils import (
    graph as g,
)


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    return common.evaluate_until_handled(
        graph,
        n_id,
        ctx=ctx,
        evaluate=evaluate,
        evaluators=(
            _evaluate_case_1,
            _evaluate_case_2,
        )
    )


def _evaluate_case_1(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: Context,
) -> Context:
    match = g.match_ast(graph, n_id, '__0__', 'LPAREN', '__1__', 'RPAREN')

    # pylint: disable=used-before-assignment
    if (
        (method_id := match['__0__'])
        and match['LPAREN']
        and match['RPAREN']
        and graph.nodes[method_id]['label_type'] in {
            'CustomIdentifier',
            'IdentifierRule',
        }
    ):
        if args_id := match['__1__']:
            args_ctx = generic.evaluate(graph, args_id, ctx=None)
            common.merge_contexts(ctx, args_ctx)
            args = args_ctx.statements
        else:
            args = []

        ctx.statements.append(StatementCustomMethodInvocation(
            meta=get_default_statement_meta(),
            method=graph.nodes[method_id]['label_text'],
            stack=args,
        ))
        common.mark_if_sink(graph, n_id, ctx)
    else:
        raise common.NotHandled()

    return ctx


def _evaluate_case_2(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: Context,
) -> Context:
    match = g.match_ast(
        graph,
        n_id,
        '__0__',
        'CustomIdentifier',
        'LPAREN',
        '__1__',
        'RPAREN',
    )

    # pylint: disable=used-before-assignment
    if (
        (chain_id := match['__0__'])
        and graph.nodes[chain_id]['label_type'] in {
            'CustomMethodInvocation_lfno_primary',
        }
        and (method_id := match['CustomIdentifier'])
        and match['LPAREN']
        and match['RPAREN']
    ):
        chain_ctx = generic.evaluate(graph, chain_id, ctx=None)
        common.merge_contexts(ctx, chain_ctx)

        if args_id := match['__1__']:
            args_ctx = generic.evaluate(graph, args_id, ctx=None)
            common.merge_contexts(ctx, args_ctx)
            args = args_ctx.statements
        else:
            args = []

        ctx.statements.append(StatementCustomMethodInvocationChain(
            meta=get_default_statement_meta(),
            method=graph.nodes[method_id]['label_text'],
            stacks=[
                chain_ctx.statements,
                args,
            ],
        ))

        common.mark_if_sink(graph, n_id, ctx)
    else:
        raise common.NotHandled()

    return ctx
