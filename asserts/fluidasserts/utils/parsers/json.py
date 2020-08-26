# -*- coding: utf-8 -*-
"""Fluid Asserts JSON parser."""

# standard imports
from collections import UserDict
from collections import UserList
from typing import Any

# 3rd party imports
from lark import Lark
from lark import Transformer
from lark import Tree
from lark import v_args


class CustomList(UserList):  # pylint: disable=too-many-ancestors
    """Custom List that allows access to the line where each node is."""

    def __init__(self, initlist, line: int = None):
        """Initialize a custom list."""
        super().__init__(initlist)
        if line:
            setattr(self, '__line__', line)

    def __getitem__(self, index):
        """Change behavior when getting an object."""
        result = None
        tokens = []
        if isinstance(index, str):
            tokens = index.split('.')
            index = int(tokens[0])
        if len(tokens) == 2 and tokens[1] == 'line':
            if '__line__' in self.data[index]:
                result = self.data[index]['__line__']
            else:
                result = self.data[index].__line__
        elif isinstance(self.data[index], (CustomList, list)):
            result = self.data[index]
        elif '__item__' in self.data[index]:
            return self.data[index]['__item__']
        else:
            return self.data[index]

        return result


class CustomDict(UserDict):  # pylint: disable=too-many-ancestors
    """Custom dictionary that allows access to the line where each node is."""

    def __setitem__(self, key, item):
        """Change behavior when adding an object."""
        line = None
        if isinstance(key, tuple):
            line = key[1]
            key = key[0]
        if isinstance(item, Tree):
            if item.data == 'false':
                self.data[key] = {'__item__': False, '__line__': item.line}
            elif item.data == 'true':
                self.data[key] = {'__item__': True, '__line__': item.line}
            elif item.data == 'null':
                self.data[key] = {'__item__': None, '__line__': item.line}
            elif item.data == 'array':
                for index, element in enumerate(item.children):
                    item.children[index] = CustomList(
                        element.children, item.line) if isinstance(
                            element, Tree) else element
                self.data[key] = CustomList(item.children, item.line)
        elif isinstance(item, (dict, CustomDict, CustomList, list)):
            if line:
                setattr(item, '__line__', line)
            super().__setitem__(key, item)
        else:
            super().__setitem__(key, item)

    def get(self, key, default=None):
        """Change behavior when getting an object."""
        result = None
        if key in self.data and '__item__' in self.data[key]:
            result = self.data[key]['__item__']
        elif key in self.data:
            result = self.data[key]
        else:
            result = default
        return result

    def __getitem__(self, key):
        """Change behavior when getting an object."""
        result = None
        if isinstance(
                key,
                str) and '.line' in key and key.split('.')[0] in self.data:
            if '__line__' in self.data[key.split('.')[0]]:
                result = self.data[key.split('.')[0]]['__line__']
            else:
                result = self.data[key.split('.')[0]].__line__
        if key in self.data:
            if key == '__line__':
                result = self.data.get('__line__')
            elif '__item__' in self.data:
                result = self.data['__item__']
            elif '__item__' in self.data[key]:
                result = self.data[key]['__item__']
            else:
                result = self.data[key]
        return result


class TreeToJson(Transformer):
    """Convert Tree Lark in a JSON Object."""

    @v_args(inline=True)
    def string(self, tree):  # pylint: disable=no-self-use
        """Convert string values."""
        return CustomDict({
            '__item__': tree[1:-1].replace('\\"', '"'),
            '__line__': tree.line
        })

    @v_args(inline=True)
    def string_(self, tree):  # pylint: disable=no-self-use
        """Convert string keys."""
        return (tree[1:-1].replace('\\"', '"'), tree.line)

    pair = tuple
    object = CustomDict

    @v_args(inline=True)
    def number(self, tree):  # pylint: disable=no-self-use
        """Convert number values."""
        return CustomDict({'__item__': float(tree), '__line__': tree.line})


def parse(json_string: str):
    """Parse a JSON string to a dict object."""
    json_grammar = r"""
        ?start: value

        ?value: object
              | array
              | string
              | SIGNED_NUMBER      -> number
              | "true"             -> true
              | "false"            -> false
              | "null"             -> null

        array  : "[" [value ("," value)*] "]"
        object : "{" [pair ("," pair)*] "}"
        pair   : string_ ":" value

        string : ESCAPED_STRING
        string_ : ESCAPED_STRING

        %import common.ESCAPED_STRING
        %import common.SIGNED_NUMBER
        %import common.WS

        %ignore WS
    """
    json_parser = Lark(
        json_grammar,
        parser='lalr',
        lexer='standard',
        propagate_positions=True,
        maybe_placeholders=False,
        transformer=TreeToJson())

    return json_parser.parse(json_string)


def standardize_objects(obj: Any):
    """Combert custom objects to standar objects."""
    if isinstance(obj, CustomList):
        obj = list(obj)
    elif isinstance(obj, CustomDict):
        obj = dict(obj)
    return obj
