# -*- coding: utf-8 -*-

# pylint: disable=too-many-lines
# pylint: disable=too-many-ancestors
# pylint: disable=unexpected-special-method-signature
# pylint: disable=super-init-not-called

"""This module provide tools to convert Cloudformation templates in graphs."""

# standar imports
import re
from collections import OrderedDict
from collections import UserDict
from collections import UserList
import datetime
from typing import Tuple

# 3rd party imports
from grapheekdb.client.api import ProxyGraph
from grapheekdb.client.api import ProxyNode

# local imports
from fluidasserts.helper.aws import _random_string
from fluidasserts.helper.aws import get_line
from fluidasserts.utils.parsers.json import CustomDict
from fluidasserts.utils.parsers.json import CustomList


def create_alias(name: str, randoms=False) -> str:
    """Create an alias for Cipher statement.

    :param randoms: Add random chars to alias.
    """
    alias = name.replace('-', '_').lower().replace('::', '_').replace(
        ':', '_').replace('.', '_')
    if randoms:
        alias = f'{alias}_{_random_string(5)}'
    return alias


def _get_line(object_, key):
    line = None
    try:
        line = object_[f'{key}.line']
    except (KeyError, TypeError, AttributeError):
        try:
            line = get_line(object_[key])
        except KeyError:
            line = 0
        if line == 0:
            line = get_line(object_)
    return line if line != 0 else None


def is_primitive(item) -> bool:
    """Check if an object is of primitive type."""
    return not hasattr(item, '__dict__') and not isinstance(item, (list))


def _create_label(key: str) -> Tuple[str]:
    return (key.replace('-', '_').replace('::', ':').replace(' ', '_').replace(
        '.', '__').split(':')[-1], key)


class List(UserList):
    """Custom list that passes items to neo4j nodes."""

    def __init__(self, initlist, father_node: ProxyNode, graph: ProxyGraph,
                 line, **kwargs):
        """Convert input list to noe4j nodes.

        :param initlist: Input list.
        :param father_id: Id of parent node.
        :param session: Neo4j session.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.graph = graph
        self.__node__ = self.graph.add_node(kind='Array', line=line)
        self.graph.add_edge(father_node, self.__node__, action='HAS')

        super().__init__(initlist)
        for index, item in enumerate(initlist):
            line = _get_line(initlist, index) or line
            self.__setitem__(index, item, line)

    def __setitem__(self, index, item, line):
        node = self.__create_node__(index, item, line)
        attrs = {
            '__references__': self.__references__,
            '__path__': self.__path__
        }
        if is_primitive(item):
            self.data[index] = item
        elif isinstance(item, (list, CustomList)):
            self.data[index] = List(
                item, father_node=node, graph=self.graph, line=line, **attrs)
        elif isinstance(item, (dict, CustomDict)):
            self.data[index] = Dict(
                item, graph=self.graph, node=node, line=line, **attrs)

    def __create_node__(self, index, item, line):
        """Converts a list item to a neo4j node."""
        attrs = {'line': line, 'index': index}
        if is_primitive(item):
            attrs.update({'value': item})
        node = self.graph.add_node(kind='Item', **attrs)
        self.graph.add_edge(self.__node__, node, action='HAS')
        return node


class Dict(UserDict):
    """Custom dict that passes objects to neo4j nodes."""

    def __init__(self,
                 initial_dict,
                 graph: ProxyGraph,
                 path: str = None,
                 node: int = None,
                 line: int = 0,
                 **kwargs):
        """Convert input dictionary to neo4j nodes.

        :param initial_dict: Initial dictionary.
        :param path: Path of cloudformation template.
        :param connection: Connection string to neo4j.
        :param session: Neo4j session.
        """
        # add additional properties
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.__references__ = getattr(self, '__references__', dict())
        self.__line__ = line
        self.graph = graph
        self.data = dict()

        # create template node
        if path:
            self.__path__ = path
            self.__node__ = self.graph.add_node(
                kind='CloudFormationTemplate', path=self.__path__)
        else:
            self.__node__ = node

        for key, value in initial_dict.items():
            self.__line__ = _get_line(initial_dict, key) or self.__line__
            self.__setitem__(key, value, self.__line__)

    def __setitem__(self, key: str, item, line):
        if key.startswith('__'):
            return
        attrs = {
            '__node_name__': key,
            '__references__': self.__references__,
            '__path__': self.__path__
        }
        node = self.__create_node__(key, item, line)
        if is_primitive(item):
            if key == 'Type' and hasattr(self, '__node_name__'):
                self.__references__[self.__node_name__] = self.__node__
                if re.fullmatch(r'AWS::(\w+|::)+', item):
                    label = _create_label(item)[0]
                    self.__node__.update(kind=label)
            self.data[key] = item
        elif isinstance(item, (OrderedDict, CustomDict)):
            self.data[key] = Dict(
                item, graph=self.graph, node=node, line=self.__line__, **attrs)
        elif isinstance(item, (list, CustomList, List)):
            self.data[key] = List(
                item, father_node=node, graph=self.graph, line=line, **attrs)

    def __create_node__(self, key: str, item, line: int):
        """Converts a dictionary node to a neo4j node."""
        label, original = _create_label(key)
        attrs = {'line': line, 'name': original}
        relation = 'HAS'
        if is_primitive(item):
            if isinstance(item, (datetime.date)):
                item = str(item)
            attrs.update({'value': item})
        if key.startswith('Fn::') or key == 'Ref':
            relation = 'EXECUTE'
        node = self.graph.add_node(kind=label, **attrs)
        self.graph.add_edge(self.__node__, node, action=relation)
        return node
