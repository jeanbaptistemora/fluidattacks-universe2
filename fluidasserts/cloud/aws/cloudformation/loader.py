# -*- coding: utf-8 -*-

# pylint: disable=too-many-ancestors
# pylint: disable=unexpected-special-method-signature
# pylint: disable=super-init-not-called
"""This module provide tools to convert Cloudformation templates in graphs."""

# standar imports
import re
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict
from collections import UserDict
from collections import UserList
from contextlib import suppress
from copy import copy
import datetime
import functools
from multiprocessing import cpu_count
from timeit import default_timer as timer
from typing import Tuple
from typing import Set
from typing import List as TList

# 3rd party imports
from pyparsing import Char
from pyparsing import nestedExpr
from pyparsing import Optional
from pyparsing import printables
from pyparsing import Suppress
from pyparsing import Word
from networkx import DiGraph
from networkx.algorithms import dfs_preorder_nodes

# local imports
from fluidasserts.helper.aws import _random_string
from fluidasserts.helper.aws import CLOUDFORMATION_EXTENSIONS
from fluidasserts.helper.aws import CloudFormationInvalidTemplateError
from fluidasserts.helper.aws import get_line
from fluidasserts.utils.generic import get_paths
from fluidasserts.helper.aws import load_cfn_template
from fluidasserts.utils.parsers.json import CustomDict
from fluidasserts.utils.parsers.json import CustomList


def create_alias(name: str, randoms=False) -> str:
    """Create an alias for gremlin statement.

    :param randoms: Add random chars to alias.
    """
    alias = name.replace('-', '_').lower().replace('::', '_').replace(
        ':', '_').replace('.', '_')
    if randoms:
        alias = f'{alias}_{_random_string(5)}'
    return alias


def _scan_sub_expresion(expresion) -> Tuple:
    printables1 = copy(printables).replace('$', '')
    printables2 = copy(printables).replace('}', '')
    grammar = Suppress(Optional(Word(printables1))) + Suppress(
        Char('$')) + Optional(
            nestedExpr(opener='{', closer='}', content=Word(printables2)))
    result = []
    for reference in grammar.scanString(expresion):
        with suppress(IndexError):
            result.append(reference[0][0][0])
    return result


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


def _create_label(key: str) -> Tuple[Set[str], str]:
    return (set(
        key.replace('-', '_').replace('::', ':').replace(' ', '_').replace(
            '.', '__').split(':')), key)


class List(UserList):
    """Custom list that passes items to grapheekdb nodes."""

    def __init__(self, initlist, father_node: int, graph: DiGraph, line,
                 **kwargs):
        """Convert input list to grapheekdb nodes.

        :param initlist: Input list.
        :param father_id: Id of parent node.
        :param graph: grapheekdb database.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.graph = graph
        self.__id__ = id(initlist)
        self.graph.add_node(self.__id__, labels={'Array'}, line=line)
        self.graph.add_edge(father_node, self.__id__, action='HAS')

        super().__init__(initlist)
        for index, item in enumerate(initlist):
            line = _get_line(initlist, index) or line
            self.__setitem__(index, item, line)

    def __setitem__(self, index, item, line):
        node_id = self.__create_node__(index, item, line)
        attrs = {
            '__references__': self.__references__,
            '__path__': self.__path__
        }
        if is_primitive(item):
            self.data[index] = item
        elif isinstance(item, (list, CustomList)):
            self.data[index] = List(
                item,
                father_node=node_id,
                graph=self.graph,
                line=line,
                **attrs)
        elif isinstance(item, (dict, CustomDict)):
            self.data[index] = Dict(
                item, graph=self.graph, node_id=node_id, line=line, **attrs)

    def __setreferences__(self):
        """Create references between nodes."""
        for item in self.data:
            if isinstance(item, (Dict)):
                item.__setreferences__()
            elif isinstance(item, (List)):
                for value in item:
                    if hasattr(value, '__setreferences__'):
                        value.__setreferences__()

    def __create_node__(self, index, item, line):
        """Converts a list item to a grapheekdb node."""
        attrs = {'line': line, 'index': index}
        if is_primitive(item):
            attrs.update({'value': item})
        _id = id(item)
        self.graph.add_node(_id, labels={'Item'}, **attrs)
        self.graph.add_edge(self.__id__, _id, action='HAS')
        return _id


class Dict(UserDict):
    """Custom dict that passes objects to grapheekdb nodes."""

    def __init__(self,
                 initial_dict,
                 graph: DiGraph,
                 path: str = None,
                 node_id: int = 0,
                 line: int = 0,
                 **kwargs):
        """Convert input dictionary to grapheekdb nodes.

        :param initial_dict: Initial dictionary.
        :param graph: grapheekdb database.
        :param path: Path of cloudformation template.
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
            self.__id__ = id(initial_dict)
            self.__path__ = path
            self.graph.add_node(
                self.__id__,
                labels={'CloudFormationTemplate'},
                path=self.__path__)
        else:
            self.__id__ = node_id

        for key, value in initial_dict.items():
            self.__line__ = _get_line(initial_dict, key) or self.__line__
            self.__setitem__(key, value, self.__line__)
        if path:
            self.__setreferences__()

    def __create_reference__(self, dest: str = None):
        """Create a reference between itself and another resource.

        :param dest: Name of resource.
        """
        if dest not in self.__references__ and re.fullmatch(
                r'AWS::(\w+|::)+', dest):
            label = _create_label(dest)[0]
            _id = id(label)
            self.graph.add_node(_id, labels=label)
            self.graph.add_edge(self.__id__, _id, action='REFERENCE')
        elif dest in self.__references__:
            ref = self.__references__[dest]
            self.graph.add_edge(self.__id__, ref, action='REFERENCE')

    def __setreferences__(self):
        """Create references between nodes."""
        for key, item in self.data.items():
            if key == 'Ref':
                self.__create_reference__(item)
            elif key == 'Fn::Sub':
                self.__fn_sub__(item)
            elif key == 'Fn::FindInMap':
                self.__fn_findinmap__(item)
            elif key == 'Fn::GetAtt':
                ref = item.split('.')[0] if isinstance(item,
                                                       (str)) else item[0]
                self.__create_reference__(ref)
            elif key.startswith('Fn'):
                pass
            elif isinstance(item, (Dict)):
                item.__setreferences__()
            elif isinstance(item, (List)):
                item.__setreferences__()

    def __fn_sub__(self, item):
        if isinstance(item, (str)):
            references = _scan_sub_expresion(item)
            for ref in references:
                self.__create_reference__(ref)

    def __fn_findinmap__(self, item):
        if isinstance(item[0], (str)):
            label = _create_label(item[0])[0]
            template = [
                _id for _id, node in self.graph.nodes.data()
                if 'CloudFormationTemplate' in node['labels']
                and node['path'] == self.__path__
            ][0]
            mappings = [
                node for node in dfs_preorder_nodes(self.graph, template, 1)
                if 'Mappings' in self.graph.nodes[node]['labels']
            ][0]
            mapping = [
                node for node in dfs_preorder_nodes(self.graph, mappings, 1)
                if self.graph.nodes[node]['labels'].intersection(label)
            ][0]
            self.graph.add_edge(self.__id__, mapping, action="REFERENCE")

    def __fn_getatt(self, item):
        ref = item.split('.')[0] if isinstance(item, (str)) else item[0]
        self.__create_reference__(ref)

    def __setitem__(self, key: str, item, line):
        if key.startswith('__'):
            return
        attrs = {
            '__node_name__': key,
            '__references__': self.__references__,
            '__path__': self.__path__
        }
        node_id = self.__create_node__(key, item, line)
        if is_primitive(item):
            if key == 'Type' and hasattr(self, '__node_name__'):
                self.__references__[self.__node_name__] = self.__id__
                if re.fullmatch(r'AWS::(\w+|::)+', item):
                    label = _create_label(item)[0]
                    labels = self.graph.nodes[self.__id__]['labels']
                    self.graph.nodes[self.__id__].update(
                        labels={*labels, *label})
            self.data[key] = item
        elif isinstance(item, (OrderedDict, CustomDict)):
            self.data[key] = Dict(
                item,
                graph=self.graph,
                node_id=node_id,
                line=self.__line__,
                **attrs)
        elif isinstance(item, (list, CustomList, List)):
            self.data[key] = List(
                item,
                father_node=node_id,
                graph=self.graph,
                line=line,
                **attrs)

    def __create_node__(self, key: str, item, line: int):
        """Converts a dictionary node to a grapheekdb node."""
        label, original = _create_label(key)
        attrs = {'line': line, 'name': original}
        relation = 'HAS'
        if is_primitive(item):
            if isinstance(item, (datetime.date)):
                item = str(item)
            attrs.update({'value': item})
        if key.startswith('Fn::') or key == 'Ref':
            relation = 'EXECUTE'
        _id = id(key)
        self.graph.add_node(_id, labels=label, **attrs)
        self.graph.add_edge(self.__id__, _id, action=relation)
        return _id

    @staticmethod
    def load_templates(
            path: str,
            graph: DiGraph,
            exclude: TList[str] = None) -> DiGraph:
        """
        Load all templates to the database.

        If you did not connect to a database use ``retry=True``.

        :param path: Path of cloudformation templates.
        :param exclude: Paths to exclude.
        """
        exclude = tuple(exclude) if exclude else None

        def load(_path_):
            template = _convert_template(_path_)
            if template:
                start_time = timer()
                success = True
                try:
                    Dict(template, path=_path_, graph=graph)
                except Exception as exc:  # pylint: disable=broad-except
                    error = str(exc)
                    success = False
                elapsed_time = timer() - start_time

                print(f'# Loading: {_path_}')
                if success:
                    print((f'#    [SUCCESS]    time: %.4f seconds') %
                          (elapsed_time))
                else:
                    print(f'#    [ERROR] {error}')

        init_time = timer()
        with ThreadPoolExecutor(max_workers=cpu_count() * 3) as worker:
            worker.map(load,
                       get_paths(
                           path,
                           exclude=exclude,
                           endswith=CLOUDFORMATION_EXTENSIONS))
        end_time = timer() - init_time
        print(f'# [SUCCESS]    Total: %.4f seconds' % (end_time))
        return graph


@functools.lru_cache(maxsize=None)
def _convert_template(path: str):
    template = None
    with suppress(CloudFormationInvalidTemplateError):
        template = load_cfn_template(path)
    return template
