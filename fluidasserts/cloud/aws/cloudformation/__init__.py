"""
Fluid Asserts AWS cloud package.

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# standard imports
from typing import Any, List, Dict, Callable, Set, Optional, Tuple, Union
from collections import namedtuple
from contextvars import ContextVar
from contextlib import contextmanager

# 3d imports
import networkx as nx
from networkx import DiGraph
from networkx.algorithms import dfs_preorder_nodes
# local imports
from fluidasserts.cloud.aws.cloudformation import services
from fluidasserts import Unit, OPEN, CLOSED
from fluidasserts.cloud.aws.cloudformation.loader import Dict \
    as ADict
from fluidasserts.helper import aws as helper

# Containers
Vulnerability = namedtuple('Vulnerability', [
    'path',
    'entity',
    'identifier',
    'reason',
    'line'], defaults=[None, None, None, None, 0])

GRAPHS = ContextVar('Graphs', default=DiGraph())


def _index(dictionary: dict, indexes: List[Any], default: Any = None) -> Any:
    """Safely Index a dictionary over indexes without KeyError opportunity."""
    if len(indexes) < 2:
        raise AssertionError('indexes length must be >= two')
    result = dictionary.get(indexes[0], {})
    for index in indexes[1:-1]:
        result = result.get(index, {})
    result = result.get(indexes[-1], default)
    return result


def _get_result_as_tuple(*,
                         vulnerabilities: List[Vulnerability],
                         msg_open: str, msg_closed: str) -> tuple:
    """Return the tuple version of the Result object."""
    # Example:
    # - where: {path}
    #   specific: {entity}/{id} {reason}

    vuln_units: List[Unit] = [
        Unit(where=f'{x.path} - [{x.identifier}] {x.entity} {x.reason}.',
             specific=[x.line])
        for x in vulnerabilities]

    if vuln_units:
        return OPEN, msg_open, vuln_units
    return CLOSED, msg_closed, vuln_units


@contextmanager
def templates_as_graph(path: str, exclude: List[str] = None) -> DiGraph:
    """Yield a graph with all the templates inside the path."""
    _graph: DiGraph = DiGraph()
    ADict.load_templates(path, _graph, exclude)
    yield _graph


def get_ref_nodes(graph: DiGraph, node: int,
                  condition: Callable = None, depth: int = 3) -> List[int]:
    """
    Returns the value of a node the value of its reference.

    If the node already has a value, the same node is returned, otherwise the
    references that meet the condition are searched.

    :param graph: Templates converted into a DiGraph.
    :param node: Id of node.
    :param condition: Condition that the reference value must meet,
        a boolean must return.
    """
    if not condition:
        def condition(  # noqa pylint: disable=function-redefined
            value): return True  # noqa pylint: disable=unused-argument,multiple-statements
    nodes: List[int] = [node] if 'value' in graph.nodes[node] and condition(
        graph.nodes[node]['value']) else [
            ref for ref in dfs_preorder_nodes(graph, node, depth)
            if 'value' in graph.nodes[ref]
            and condition(graph.nodes[ref]['value'])]
    return nx.utils.flatten(nodes)


def get_type(graph: DiGraph, node: int, allowed_types: Set[str]) -> str:
    """
    Returns the predecessor that are within the allowed types.

    :param graph: Templates converted into a DiGraph.
    :param node: Id of node.
    :param allowed_types: Nodes that can be found within the predecessors.
    """
    _type = None
    intersec = graph.nodes[node]['labels'].intersection(allowed_types)
    if intersec:
        _type = list(intersec)[-1]
    else:
        for _ in range(5):
            node = list(graph.predecessors(node))
            node = node[0]
            intersec = graph.nodes[node]['labels'].intersection(allowed_types)
            if intersec:
                _type = list(intersec)[-1]
                break
    return _type


def get_predecessor(graph: DiGraph, node: int,
                    labels: Union[Set[str], str]) -> int:
    """
    Returns the node of the first predecessor that contains the label.

    :param graph: Templates converted into a DiGraph.
    :param node: Id of node.
    :param label: Nodes that can be found within the predecessors.
    """
    predecessor = None
    if isinstance(labels, str):
        labels = {labels}
    if graph.nodes[node]['labels'].intersection(labels):
        return node
    for _ in range(12):
        if 'CloudFormationTemplate' in graph.nodes[node]['labels']:
            break
        node = list(graph.predecessors(node))[0]
        if graph.nodes[node]['labels'].intersection(labels):
            predecessor = node
            break
    return predecessor


def get_graph(path: str, exclude: Optional[List[str]] = None) -> DiGraph:
    """Returns a graph with all the templates inside the path"""
    _graph: DiGraph = GRAPHS.get()
    GRAPHS.set(ADict.load_templates(path=path, graph=_graph, exclude=exclude))
    return GRAPHS.get()


def get_templates(graph: DiGraph,
                  path: str,
                  exclude: Optional[List[str]] = None
                  ) -> List[Tuple[int, Dict]]:
    """Returns the templates that are inside a graph."""
    result: List[Tuple[int, Dict]] = []
    templates: List[Tuple[int, Dict]] = [
        (_id, node) for _id, node in graph.nodes.data()
        if 'CloudFormationTemplate' in node['labels']
    ]
    for _id, template in templates:
        t_path: str = template['path']
        if path in t_path:
            result.append((_id, template))
    if exclude:
        result = [(_id, node) for _id, node in result
                  if not any(ex in node['path'] for ex in exclude)]
    return result


def get_resources(
        graph: DiGraph,
        nodes: Union[List[int], int],
        labels: Union[Set[str], str],
        depth: int = 2,
        info: bool = False,
        num_labels: int = None) -> Union[Tuple[int, Dict, Dict], List[int]]:
    """
    Returns all the resources that those labels contain.

    :param graph: Templates converted into a graph.
    :param nodes: Main nodes.
    :param labels: Labels that the nodes to find must have.
    :param depth: Search depth.
    :param info: If the information is enabled a tuple is returned that
        continues (node_id, node, template).
    """
    if isinstance(nodes, int):
        nodes = [nodes]
    if isinstance(labels, str):
        labels = {labels}
    if not num_labels:
        num_labels = len(labels)
    labels = {label.replace('-', '_') for label in labels}
    if info:
        return [
            (node, graph.nodes[node], graph.nodes[get_predecessor(
                graph, node, 'CloudFormationTemplate')])
            for x in nodes for node in dfs_preorder_nodes(
                graph, x, depth)
            if len(graph.nodes[node]['labels'].intersection(
                labels)) >= num_labels
        ]
    return [
        node for x in nodes for node in dfs_preorder_nodes(graph, x, depth)
        if len(graph.nodes[node]['labels'].intersection(labels)) >= num_labels
    ]


def has_values(graph: DiGraph,
               nodes: Union[List[int], int],
               labels: Union[Set[str], str],
               values: Union[List[Any], Any],
               depth: int = 2,
               full_match: bool = False) -> List[int]:
    """
    Validate if there are nodes whose value is within the indicated values.

    :param graph: Templates converted into a graph.
    :param nodes: Main nodes.
    :param labels: Labels that the nodes to find must have.
    :param values: Values that the nodes must have.
    :param depth: Search depth.
    :param full_match: The value of the nodes must match completely.
    """
    results: List[int] = []
    if isinstance(nodes, int):
        nodes = [nodes]
    if isinstance(labels, str):
        labels = {labels}
    if not isinstance(values, List):
        values = [values]
    resources = get_resources(graph, nodes, labels, depth=depth)
    references = nx.utils.flatten(
        [get_ref_nodes(graph, resource) for resource in resources])
    for ref in references:
        success = False
        if 'value' in graph.nodes[ref]:
            node_value = graph.nodes[ref]['value']
            if not full_match:
                try:
                    success = any(node_value in val for val in values)
                except TypeError:
                    success = any(val == node_value for val in values)
            else:
                success = any(val == node_value for val in values)
        if success:
            results.append(ref)
    return results


def get_list_node_items(graph: DiGraph, node: int, label: str, depth: int):
    """Returns a list with the values, or value, of a value/list type node."""
    _items = helper.get_index(get_resources(graph,
                                            node,
                                            label,
                                            depth=depth), 0)
    value = get_value(graph, _items)
    items: List = []
    if value:
        items = [value]
    else:
        items = get_resources(graph,
                              _items,
                              'Item',
                              depth=depth)
    return items


def policy_statement_privilege(graph: DiGraph, statement: int, effect: str,
                               action: str):
    """Check if a statement of a policy allow an action in all resources.

    :param statemet: policy statement.
    :param effect: (Allow | Deny)
    :param action: (read | list | write | tagging | permissions_management)
    """
    writes: List[bool] = []
    effects = has_values(graph, statement, 'Effect', effect, 5)
    for eff in effects:
        father = list(graph.predecessors(eff))
        resource = helper.get_index(
            get_resources(graph, father, 'Resource'), 0)
        action_node = helper.get_index(
            get_resources(graph, father, 'Action'), 0)
        if resource and helper.resource_all_(graph, resource) and action_node:
            writes.append(
                policy_actions_has_privilege(graph, action_node, action))
    return any(writes)


def policy_actions_has_privilege(graph: DiGraph, action: int,
                                 privilege) -> bool:
    """Check if an action have a privilege."""
    write_actions: dict = services.ACTIONS
    success = False

    action_node = graph.nodes[action]
    if 'value' in action_node:
        if action_node['value'] == '*':
            success = True
        else:
            actions = []
            serv, act = action_node['value'].split(':')
            if act.startswith('*'):
                actions.append(True)
            else:
                act = act[:act.index('*')] if act.endswith('*') else act
                actions.append(act in write_actions.get(
                    serv, {}).get(privilege, []))
            success = any(actions)

    else:
        nodes = list(dfs_preorder_nodes(graph, action))
        success = any(
            policy_actions_has_privilege(graph, node, privilege)
            for node in nodes[1:])
    return success


def get_value(graph: DiGraph,
              node: int):
    """Returns value of graph node"""
    if 'value' in graph.nodes.get(node):
        value = graph.nodes.get(node)['value']
    else:
        value = None
    return value
