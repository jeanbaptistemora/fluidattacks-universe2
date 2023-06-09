from collections.abc import (
    Callable,
    Iterable,
    Iterator,
)
from itertools import (
    chain,
)
from jmespath import (
    search as jsh,
)
from model import (
    core_model,
)
from model.graph_model import (
    Graph,
    NAttrs,
    NAttrsPredicateFunction,
    NId,
    NIdPredicateFunction,
)
import networkx as nx
import os
from typing import (
    Any,
)
from utils.logs import (
    log_blocking,
)
from utils.system import (
    read_blocking,
)

# Constants
CFG = dict(label_cfg="CFG")
ALWAYS = dict(**CFG, label_cfg_always="cfg_always")
BREAK = dict(**CFG, label_cfg_break="cfg_break")
CONTINUE = dict(**CFG, label_cfg_continue="cfg_continue")
FALSE = dict(**CFG, label_cfg_false="cfg_false")
MAYBE = dict(**CFG, label_cfg_maybe="cfg_maybe")
TRUE = dict(**CFG, label_cfg_true="cfg_true")
GRAPH_STYLE_ATTRS = {"arrowhead", "color", "fillcolor", "label", "style"}
ROOT_NODE: str = "1"


def to_svg(graph: Graph, path: str) -> bool:
    nx.drawing.nx_agraph.write_dot(graph, path)

    code, _, stderr = read_blocking("dot", "-O", "-T", "svg", path)

    if code == 0:
        os.unlink(path)
        return True

    log_blocking("debug", "Error while generating svg: %s", stderr.decode())
    return False


def has_labels(n_attrs: NAttrs, **expected_attrs: str) -> bool:
    return all(
        n_attrs.get(expected_attr) == expected_attr_value
        for expected_attr, expected_attr_value in expected_attrs.items()
    )


def pred_has_labels(**expected_attrs: str) -> NAttrsPredicateFunction:
    def predicate(n_attrs: NAttrs) -> bool:
        return has_labels(n_attrs, **expected_attrs)

    return predicate


def filter_nodes(
    graph: Graph,
    nodes: Iterable[str],
    predicate: NAttrsPredicateFunction,
) -> tuple[str, ...]:
    result: tuple[str, ...] = tuple(
        n_id for n_id in nodes if predicate(graph.nodes[n_id])
    )

    return result


def matching_nodes(graph: Graph, **expected_attrs: str) -> tuple[str, ...]:
    return filter_nodes(graph, graph.nodes, pred_has_labels(**expected_attrs))


def adj_lazy(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    strict: bool = False,
    _processed_n_ids: set[str] | None = None,
    **edge_attrs: str,
) -> Iterator[str]:
    """Return adjacent nodes to `n_id`, following just edges with given attrs.

    - Parameter `depth` may be -1 to indicate infinite depth.
    - Parameter `strict` indicates that the edges must have only the indicated
      attributes

    - Search is done breadth first.
    - Nodes are returned ordered ascending by index on each level.

    This function must be used instead of graph.adj, because graph.adj
    becomes unstable (unordered) after mutating the graph, also this allow
    following just edges matching `edge_attrs`.
    """
    processed_n_ids: set[str] = _processed_n_ids or set()
    if depth == 0 or n_id in processed_n_ids:
        return

    processed_n_ids.add(n_id)

    childs: list[str] = sorted(graph.adj[n_id], key=int)

    edge_keys = set(edge_attrs.keys())

    # Append direct childs
    for c_id in childs:
        process = has_labels(graph[n_id][c_id], **edge_attrs)
        if strict and process:
            graph_edge_keys = set(graph[n_id][c_id].keys())
            difference = graph_edge_keys.difference(edge_keys)
            process = not bool(difference) or difference == {"label_index"}
        if process:
            yield c_id

    # Recurse into childs
    if depth < 0 or depth > 1:
        for c_id in childs:
            process = has_labels(graph[n_id][c_id], **edge_attrs)
            if process and strict:
                graph_edge_keys = set(graph[n_id][c_id].keys())
                difference = graph_edge_keys.difference(edge_keys)
                process = not bool(difference) or difference == {"label_index"}
            if process:
                yield from adj_lazy(
                    graph,
                    c_id,
                    depth=depth - 1,
                    strict=strict,
                    _processed_n_ids=processed_n_ids,
                    **edge_attrs,
                )


def adj(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    strict: bool = False,
    _processed_n_ids: set[str] | None = None,
    **edge_attrs: str,
) -> tuple[str, ...]:
    return tuple(
        adj_lazy(
            graph,
            n_id,
            depth=depth,
            strict=strict,
            _processed_n_ids=_processed_n_ids,
            **edge_attrs,
        )
    )


def adj_ast(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    strict: bool = False,
    **n_attrs: str,
) -> tuple[Any, ...]:
    return tuple(
        c_id
        for c_id in adj(graph, n_id, depth, strict=strict, label_ast="AST")
        if has_labels(graph.nodes[c_id], **n_attrs)
    )


def adj_ctx(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    strict: bool = False,
    **n_attrs: str,
) -> tuple[Any, ...]:
    return tuple(
        c_id
        for c_id in adj(graph, n_id, depth, strict=strict, label_ctx="CTX")
        if has_labels(graph.nodes[c_id], **n_attrs)
    )


def adj_cfg(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    strict: bool = False,
    **n_attrs: str,
) -> tuple[Any, ...]:
    return tuple(
        c_id
        for c_id in adj(graph, n_id, depth, strict=strict, label_cfg="CFG")
        if has_labels(graph.nodes[c_id], **n_attrs)
    )


def adj_cfg_lazy(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    strict: bool = False,
    **n_attrs: str,
) -> Iterator[Any]:
    yield from adj_lazy(
        graph,
        n_id,
        depth=depth,
        strict=strict,
        _processed_n_ids=set(),
        label_cfg="CFG",
        **n_attrs,
    )


def pred_lazy(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    _processed_n_ids: set[str] | None = None,
    **edge_attrs: str,
) -> Iterator[str]:
    """Same as `adj` but follow edges in the opposite direction."""
    processed_n_ids: set[str] = _processed_n_ids or set()
    if depth == 0 or n_id in processed_n_ids:
        return

    processed_n_ids.add(n_id)

    p_ids: list[str] = sorted(graph.pred[n_id], key=int)

    # Append direct parents
    for p_id in p_ids:
        if has_labels(graph[p_id][n_id], **edge_attrs):
            yield p_id

    # Recurse into parents
    if depth < 0 or depth > 1:
        for p_id in p_ids:
            if has_labels(graph[p_id][n_id], **edge_attrs):
                yield from pred_lazy(
                    graph,
                    p_id,
                    depth=depth - 1,
                    _processed_n_ids=processed_n_ids,
                    **edge_attrs,
                )


def pred(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    _processed_n_ids: set[str] | None = None,
    **edge_attrs: str,
) -> tuple[str, ...]:
    return tuple(
        pred_lazy(
            graph,
            n_id,
            depth,
            _processed_n_ids=_processed_n_ids,
            **edge_attrs,
        )
    )


def pred_ast(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> tuple[str, ...]:
    return tuple(pred_ast_lazy(graph, n_id, depth, **edge_attrs))


def pred_ast_lazy(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Iterator[str]:
    yield from pred_lazy(
        graph,
        n_id,
        depth,
        _processed_n_ids=set(),
        label_ast="AST",
        **edge_attrs,
    )


def pred_cfg(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> tuple[str, ...]:
    return tuple(pred_cfg_lazy(graph, n_id, depth, **edge_attrs))


def pred_cfg_lazy(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Iterator[str]:
    yield from pred_lazy(
        graph,
        n_id,
        depth,
        _processed_n_ids=set(),
        label_cfg="CFG",
        **edge_attrs,
    )


def paths(
    graph: Graph,
    s_id: str,
    t_id: str,
    **edge_attrs: str,
) -> tuple[tuple[str, ...], ...]:
    return tuple(_paths(graph, s_id, t_id, **edge_attrs))


def _paths(
    graph: Graph,
    s_id: str,
    t_id: str,
    **edge_attrs: str,
) -> Iterator[tuple[str, ...]]:
    t_ids = {t_id}

    if s_id in t_ids:
        return

    visited: dict[str, None] = dict.fromkeys([s_id])
    pending = [(s_id, iter(graph[s_id]))]

    while pending:
        pending_s_id, pending_ids = pending[-1]
        child = next(pending_ids, None)

        if child is None:
            pending.pop()
            visited.popitem()

        elif len(visited) + 1 < len(graph):
            if (
                # Already visited
                child in visited
                # Does not match the criteria
                or not has_labels(graph[pending_s_id][child], **edge_attrs)
            ):
                continue

            if child in t_ids:
                yield tuple(visited) + (child,)

            visited[child] = None
            if t_ids - set(visited):
                pending.append((child, iter(graph[child])))
            else:
                visited.popitem()
        else:
            for n_id in (t_ids & (set(pending_ids) | {child})) - set(visited):
                yield tuple(visited) + (n_id,)
            pending.pop()
            visited.popitem()


def get_node_cfg_condition(graph: Graph, n_id: str) -> str:
    p_id = graph.nodes[n_id]["label_parent_ast"]
    val: str

    for key, val in graph[p_id][n_id].items():
        if key.startswith("label_cfg_"):
            return val

    return "cfg_never"


def match_ast(
    graph: Graph,
    n_id: str,
    *label_type: str,
    depth: int = 1,
) -> dict[str, str | None]:
    index: int = 0
    nodes: dict[str, str | None] = dict.fromkeys(label_type)

    for c_id in adj_ast(graph, n_id, depth=depth):
        c_type = graph.nodes[c_id]["label_type"]
        if c_type in nodes and nodes[c_type] is None:
            nodes[c_type] = c_id
        else:
            nodes[f"__{index}__"] = c_id
            index += 1

    return nodes


def match_ast_d(
    graph: Graph,
    n_id: str,
    label_type: str,
    depth: int = 1,
) -> str | None:
    return match_ast(graph, n_id, label_type, depth=depth)[label_type]


def match_ast_group(
    graph: Graph,
    n_id: str,
    *label_type: str,
    depth: int = 1,
) -> dict[str, list[str]]:
    index: int = 0
    nodes: dict[str, list[str]] = {label: [] for label in label_type}

    for c_id in adj_ast(graph, n_id, depth=depth):
        c_type = graph.nodes[c_id]["label_type"]
        if c_type in nodes:
            nodes[c_type].append(c_id)
        else:
            nodes[f"__{index}__"] = c_id
            index += 1

    return nodes


def match_ast_group_d(
    graph: Graph,
    n_id: str,
    label_type: str,
    depth: int = 1,
) -> list[str]:
    return match_ast_group(graph, n_id, label_type, depth=depth)[label_type]


def get_ast_childs(
    graph: Graph,
    n_id: NId,
    label_type: str,
    *,
    depth: int = 1,
) -> tuple[NId, ...]:
    return tuple(
        n_id
        for n_id in adj_ast(graph, n_id, depth=depth)
        if graph.nodes[n_id]["label_type"] == label_type
    )


def is_connected_to_cfg(graph: Graph, n_id: NId) -> bool:
    return bool(adj_cfg(graph, n_id) or pred_cfg(graph, n_id))


def lookup_first_cfg_parent(
    graph: Graph,
    n_id: NId,
) -> str:
    # Lookup first parent who is connected to the CFG
    for p_id in chain([n_id], pred_ast_lazy(graph, n_id, depth=-1)):
        if is_connected_to_cfg(graph, p_id):
            return p_id

    # Base case, pass through
    return n_id


def ast_filter_sink_connected_n_ids(
    graph: Graph, n_id: NId, finding: core_model.FindingEnum, only_sinks: bool
) -> tuple[str, ...]:
    # Compute all childs reachable from CFG edges
    c_ids = adj_cfg(graph, n_id, depth=-1)

    # Filter nodes that are connected to a sink via the AST
    return tuple(
        sorted(
            {
                c_id
                for c_id in chain([n_id], c_ids)
                if (
                    # The node's sink match the finding name
                    finding.name
                    in graph.nodes[c_id].get("label_sink_type", {})
                    # The node has an AST child that is a sink of the finding
                    or any(
                        finding.name
                        in graph.nodes[c_c_id].get("label_sink_type", {})
                        for c_c_id in adj_ast(graph, c_id, depth=-1)
                    )
                    # The node is and leaf node
                    or (not only_sinks and not adj_cfg(graph, c_id))
                )
            },
            key=int,
        )
    )


def branches_cfg(
    graph: Graph,
    n_id: NId,
    finding: core_model.FindingEnum,
    only_sinks: bool = False,
) -> tuple[tuple[str, ...], ...]:

    # Temporarily connect function call nodes with function declaration
    # nodes if a sink is present inside the function.
    call_dcl_map = {
        call_id: dcl_id
        for call_id in adj_cfg(graph, n_id, depth=-1)
        if (
            (dcl_id := graph.nodes[call_id].get("label_function_declaration"))
            and any(
                finding.name
                in graph.nodes[dcl_c_id].get("label_sink_type", {})
                for dcl_c_id in adj_ast(graph, dcl_id, depth=-1)
            )
        )
    }
    for s_id, e_id in call_dcl_map.items():
        graph.add_edge(s_id, e_id, **ALWAYS)
        graph.add_edge(s_id, e_id, label_ast="AST")

    target_ids = ast_filter_sink_connected_n_ids(
        graph, n_id, finding, only_sinks
    )

    # If a target_id is CFG-reachable from another target_id, remove it
    # because its information is already contained within the path of the other
    target_ids = tuple(
        {
            target_id
            for index, target_id in enumerate(target_ids)
            if all(
                target_id_leaf != other_target_id
                for target_id_leaf in adj_cfg_lazy(graph, target_id, depth=-1)
                for other_target_id in target_ids[index + 1 :]
                if target_id != other_target_id
            )
        }
    )
    # All branches, may be duplicated, some branches may be prefix of others
    branches: set[tuple[str, ...]] = set(
        path
        for leaf_id in target_ids
        for path in (
            [(n_id,)]
            if n_id == leaf_id
            else paths(graph, n_id, leaf_id, label_cfg="CFG")
        )
    )

    # Deduplicate, merge prefixes and return branches
    result: tuple[tuple[str, ...], ...] = tuple(sorted(branches))

    # Remove temporary edges connecting function calls with their declarations
    for s_id, e_id in call_dcl_map.items():
        graph.remove_edge(s_id, e_id)
    return result


def import_graph_from_json(model: Any) -> Graph:
    graph = Graph()

    for n_id, n_attrs in model["nodes"].items():
        graph.add_node(n_id, **n_attrs)
        for csv_label in ("label_input_type", "label_sink_type"):
            if csv_label in graph.nodes[n_id]:
                graph.nodes[n_id][csv_label] = set(
                    graph.nodes[n_id][csv_label].split(",")
                )

    for n_id_from, n_id_from_value in model["edges"].items():
        for n_id_to, edge_attrs in n_id_from_value.items():
            graph.add_edge(n_id_from, n_id_to, **edge_attrs)

    return graph


def export_graph_as_json(
    graph: Graph,
    *,
    include_styles: bool = False,
) -> dict[str, Any]:
    data: dict[str, Any] = {}
    data["nodes"] = {}
    data["edges"] = {}
    ignored_attrs = GRAPH_STYLE_ATTRS

    for n_id, n_attrs in graph.nodes.items():
        data["nodes"][n_id] = n_attrs.copy()
        for csv_label in ("label_input_type", "label_sink_type"):
            if csv_label in data["nodes"][n_id]:
                data["nodes"][n_id][csv_label] = ",".join(
                    sorted(data["nodes"][n_id][csv_label])
                )

        if not include_styles:
            for attr in ignored_attrs:
                data["nodes"][n_id].pop(attr, None)

    for n_id_from, n_id_to in graph.edges:
        data["edges"].setdefault(n_id_from, {})
        data["edges"][n_id_from][n_id_to] = graph[n_id_from][n_id_to].copy()

        if not include_styles:
            for attr in ignored_attrs:
                data["edges"][n_id_from][n_id_to].pop(attr, None)

    return data


def _get_subgraph(
    graph: Graph,
    node_n_id_predicate: NIdPredicateFunction = lambda n_id: True,
    edge_n_attrs_predicate: NAttrsPredicateFunction = lambda n_attrs: True,
) -> Graph:
    copy: Graph = Graph()

    for n_a_id, n_b_id in graph.edges:
        edge_attrs = graph[n_a_id][n_b_id].copy()
        n_a_attrs = graph.nodes[n_a_id].copy()
        n_b_attrs = graph.nodes[n_b_id].copy()

        if (
            edge_n_attrs_predicate(edge_attrs)
            and node_n_id_predicate(n_a_id)
            and node_n_id_predicate(n_b_id)
        ):
            copy.add_node(n_a_id, **n_a_attrs)
            copy.add_node(n_b_id, **n_b_attrs)
            copy.add_edge(n_a_id, n_b_id, **edge_attrs)

    return copy


def copy_ast(graph: Graph) -> Graph:
    return _get_subgraph(
        graph=graph,
        edge_n_attrs_predicate=pred_has_labels(label_ast="AST"),
    )


def copy_cfg(graph: Graph) -> Graph:
    return _get_subgraph(
        graph=graph,
        edge_n_attrs_predicate=pred_has_labels(label_cfg="CFG"),
    )


def contains_label_type_in(
    graph: Graph,
    c_ids: tuple[str, ...],
    label_types: set[str],
) -> bool:
    return all(
        graph.nodes[c_id].get("label_type") in label_types for c_id in c_ids
    )


def concatenate_label_text(
    graph: Graph,
    c_ids: tuple[str, ...],
    separator: str | None = None,
) -> str:
    return (separator or "").join(
        graph.nodes[c_id]["label_text"] for c_id in c_ids
    )


# Functions below should disappear


def symbolic_evaluate(value: Any) -> Any:
    """Evaluate a list of expressions, return a possibly simplified equivalent.

    Examples:

        >>> [StringLiteral, ADD, StringLiteral, ADD, StringLiteral]
        StringLiteral
    """
    # Only a list of expressions can be evaluated
    if not isinstance(value, list):
        return value

    # Recursively simplify the element
    value = list(map(symbolic_evaluate, value))

    # Value is composed from 'StringLiterals' joined by 'ADD'
    if set(jsh("[0::2].type", value)) == {"StringLiteral"} and set(
        jsh("[1::2].type", value)
    ) == {"ADD"}:
        final = value[0]
        final["text"] = '"' + "".join(t["text"][1:-1] for t in value) + '"'
        return final

    return value


def simplify(value: Any) -> Any:
    """Access single node elements in order to flatten a graph.

    Examples:

        >>> simplify([{'a': 1}]) == {'a': 1}

        >>> simplify({'a': []}) == []
    """
    if isinstance(value, list):
        if len(value) == 1:
            return simplify(value[0])
        return list(map(simplify, value))

    if isinstance(value, dict):
        if len(value) == 1:
            (child_val,) = value.values()
            return simplify(child_val)
        return dict(zip(value.keys(), map(simplify, value.values())))

    return value


def yield_nodes_with_key(*, key: str, node: Any) -> Iterator[Any]:
    yield from yield_nodes(
        key_predicates=(key.__eq__,),
        post_extraction=(),
        pre_extraction=(),
        value=node,
    )


def yield_nodes(
    *,
    key: str = "__root__",
    value: Any,
    key_predicates: tuple[Callable[[str], bool], ...] = (),
    value_extraction: str = "@",
    value_predicates: tuple[str, ...] = (),
    pre_extraction: tuple[Callable[[Any], Any], ...] = (
        simplify,
        symbolic_evaluate,
    ),
    post_extraction: tuple[Callable[[Any], Any], ...] = (
        simplify,
        symbolic_evaluate,
    ),
) -> Iterator[Any]:
    """Recursively scan the graph and yield nodes that match the predicates."""

    def _yield_if_matches() -> Iterator[Any]:
        if all(jsh(pred, value) for pred in value_predicates) and all(
            pred(key) for pred in key_predicates
        ):
            to_yield = value
            for action in pre_extraction:
                to_yield = action(to_yield)
            to_yield = jsh(value_extraction, to_yield)
            for action in post_extraction:
                to_yield = action(to_yield)
            yield to_yield

    if isinstance(value, dict):
        yield from _yield_if_matches()
        for child_key, child_value in value.items():
            yield from yield_nodes(
                key=child_key,
                value=child_value,
                key_predicates=key_predicates,
                post_extraction=post_extraction,
                pre_extraction=pre_extraction,
                value_extraction=value_extraction,
                value_predicates=value_predicates,
            )
    elif isinstance(value, list):
        yield from _yield_if_matches()
        for child_key, child_value in enumerate(value):
            yield from yield_nodes(
                key=f"{key}[{child_key}]",
                value=child_value,
                key_predicates=key_predicates,
                post_extraction=post_extraction,
                pre_extraction=pre_extraction,
                value_extraction=value_extraction,
                value_predicates=value_predicates,
            )


def yield_dicts(model: Any) -> Iterator[dict[str, Any]]:
    if isinstance(model, dict):
        yield model
        for sub_model in model.values():
            yield from yield_dicts(sub_model)
    elif isinstance(model, list):
        for sub_model in model:
            yield from yield_dicts(sub_model)


def remove_cfg(graph: Graph, out_edge: str, in_edge: str) -> None:
    current_edge = {
        key: value
        for key, value in graph.edges[out_edge, in_edge].items()
        if not key.startswith("label_cfg")
    }
    graph.remove_edge(out_edge, in_edge)
    graph.add_edge(out_edge, in_edge, **current_edge)

    only_cfg = all(
        key.startswith("label_cfg") or key == "label_index"
        for key in graph.edges[out_edge, in_edge].keys()
    )
    if only_cfg:
        graph.remove_edge(out_edge, in_edge)


def get_brother_node(
    graph: Graph,
    n_id: NId,
    label_type: str,
) -> Any | None:
    parent = pred_ast(graph, n_id)[0]
    childs = adj_ast(graph, parent)
    if filtered_types := [
        id
        for id in childs[childs.index(n_id) + 1 :]
        if graph.nodes[id]["label_type"] == label_type
    ]:
        return filtered_types.pop(0)
    return None


def search_pred_until_type(
    graph: Graph,
    n_id: NId,
    targets: set[str],
    last_child: str | None = None,
) -> tuple[str, str | None]:
    if not last_child:
        last_child = n_id
    if pred_c := pred_ast(graph, n_id):
        if graph.nodes[pred_c[0]]["label_type"] in targets:
            return (pred_c[0], last_child)
        return search_pred_until_type(graph, pred_c[0], targets, pred_c[0])
    return "", ""


def get_nodes_by_path(
    graph: Graph, n_id: NId, nodes: list[NId], *label_type_path: str
) -> list[NId]:
    if len(label_type_path) == 1:
        nodes.extend(match_ast_group_d(graph, n_id, label_type_path[0]))
        return nodes
    for node in match_ast_group_d(graph, n_id, label_type_path[0]):
        get_nodes_by_path(graph, node, nodes, *label_type_path[1:])

    return nodes
