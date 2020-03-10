# -*- coding: utf-8 -*-

"""This module allows to check Python code vulnerabilities."""

# standard imports
import ast
import os
from contextlib import suppress
from typing import List, Dict

# 3rd party imports
import jmespath
from bandit import blacklists
from pyparsing import (Word, alphas, pythonStyleComment, delimitedList,
                       SkipTo, LineEnd, indentedBlock, alphanums,
                       Keyword, QuotedString, MatchFirst, Optional)

# local imports
from fluidasserts import Unit, LOW, HIGH, OPEN, CLOSED, UNKNOWN, SAST
from fluidasserts.helper import lang
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.decorators import api


LANGUAGE_SPECS = {
    'extensions': ('py',),
    'block_comment_start': None,
    'block_comment_end': None,
    'line_comment': ('#',)
}  # type: dict


# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')
# _Var_123
L_VAR_NAME = Word(alphas + '_', alphanums + '_')
# Class_123.property1.property1.value
L_VAR_CHAIN_NAME = delimitedList(L_VAR_NAME, delim='.', combine=True)


def _flatten(elements, aux_list=None):
    aux_list = aux_list if aux_list is not None else []
    for i in elements:
        if isinstance(i, list):
            _flatten(i, aux_list)
        else:
            aux_list.append(i)
    return aux_list


def _get_result_as_tuple(path: str,
                         msg_open: str,
                         msg_closed: str,
                         vulns: list = None,
                         safes: list = None) -> tuple:
    """Return the tuple version of the Result object."""
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []

    if not os.path.exists(path):
        return UNKNOWN, 'File does not exist'

    if vulns:
        vuln_units.extend(
            Unit(
                where=path_,
                specific=[x['lineno'] for x in lines],
                fingerprint=get_sha256(path_),
                source='Lines') for path_, lines in vulns)
    if safes:
        safe_units.extend(
            Unit(
                where=path_,
                specific=[0],
                fingerprint=get_sha256(path_),
                source='Lines') for path_, lines in safes)

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    if safes:
        return CLOSED, msg_closed, vuln_units, safe_units
    return CLOSED, 'No files were tested'


def is_primitive(object_):
    """Check if an object is of primitive type."""
    return not hasattr(object_, '__dict__')


def object_to_dict(object_: object):
    """Convert an object into a nested dictionary."""
    dict_ = object_.__dict__.copy()
    dict_['class_name'] = object_.__class__.__name__
    for key, value in dict_.items():
        if isinstance(value, (list, tuple, set)):
            for index, val in enumerate(value):
                value[index] = object_to_dict(val)
        if not is_primitive(value):
            dict_[key] = object_to_dict(value)
    return dict_


def iterate_dict_nodes(object_: dict):
    """Iterate nodes of an dictionary recursively."""
    yield object_
    if isinstance(object_, dict):
        for value in object_.values():
            yield from iterate_dict_nodes(value)
    elif isinstance(object_, list):
        for value in object_:
            yield from iterate_dict_nodes(value)


def execute_query(query, object_: dict):
    """
    Execute one or more queries in a dictionary.

    The queries must have the jmespath format.

    :param queries: List of Queries to execute.
    :param object_: Object on which queries are executed.
    """
    compliance = []
    if isinstance(query, str):
        query = [query]
    for node in iterate_dict_nodes(object_):
        with suppress(TypeError):
            compliance.extend([
                node
                for node in
                [jmespath.search(que, node) for que in query] if node
            ])

    return compliance


def _call_in_code(call, code_content):
    """Check if call is present in code_file."""
    code_tree = ast.parse(code_content)
    for node in code_tree.body:
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Attribute):
                    func_name = \
                        f'{node.value.func.value.id}.{node.value.func.attr}'
                else:
                    func_name = f'{node.value.func.id}'
                if call == func_name:
                    return True
    return False


def _import_in_code(import_name, code_content):
    """Check if call is present in code_file."""
    code_tree = ast.parse(code_content)
    for node in code_tree.body:
        if isinstance(node, ast.Import):
            for name in node.names:
                if import_name == name.name:
                    return True
    return False


def _insecure_functions_in_file(py_dest: str) -> Unit:
    """
    Search for insecure functions in code.

    Powered by Bandit.

    :param py_dest: Path to a Python script or package.
    """
    calls = blacklists.calls.gen_blacklist()['Call']
    imports = blacklists.imports.gen_blacklist()['Import']
    import_from = blacklists.imports.gen_blacklist()['ImportFrom']
    import_calls = blacklists.imports.gen_blacklist()['Call']

    insecure = set()

    insecure.update({y for x in calls for y in x['qualnames']})
    insecure.update({y for x in imports for y in x['qualnames']})
    insecure.update({y for x in import_from for y in x['qualnames']})
    insecure.update({y for x in import_calls for y in x['qualnames']})

    with open(py_dest, encoding='latin-1') as code_handle:
        content = code_handle.read()
    calls = [call for call in insecure
             if _call_in_code(call, content)]
    imports = [imp for imp in insecure
               if _import_in_code(imp, content)]
    results = calls + imports

    return Unit(where=py_dest,
                source='Python/Imports',
                specific=results,
                fingerprint=get_sha256(py_dest)) if results else None


def _declares_catch_for_exceptions(
        py_dest: str,
        exceptions_list: List[str],
        msgs: Dict[str, str],
        exclude: list = None) -> tuple:
    """Search for the declaration of catch for the given exceptions."""
    any_exception = L_VAR_CHAIN_NAME
    provided_exception = MatchFirst(
        [Keyword(exception) for exception in exceptions_list])

    exception_group = delimitedList(expr=any_exception, delim=',')
    exception_group.addCondition(
        # Ensure that at least one exception in the group is the provided one
        lambda tokens: any(provided_exception.matches(tok) for tok in tokens))

    grammar = Keyword('except') + Optional(
        Optional('(') + exception_group + Optional(')') + Optional(
            Keyword('as') + L_VAR_CHAIN_NAME)) + ':'
    grammar.ignore(pythonStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=py_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs=msgs,
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_generic_exceptions(py_dest: str, exclude: list = None) -> tuple:
    """
    Search for generic exceptions in a Python script or package.

    :param py_dest: Path to a Python script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        py_dest=py_dest,
        exceptions_list=[
            'Exception',
            'BaseException',
        ],
        msgs={
            OPEN: 'Code declares a "catch" for generic exceptions',
            CLOSED: 'Code does not declare "catch" for generic exceptions',
        },
        exclude=exclude)


@api(risk=LOW, kind=SAST)
def uses_catch_for_memory_error(py_dest: str, exclude: list = None) -> tuple:
    """
    Search for the use of MemoryError "catch" in a path.

    See `CWE-544 <https://cwe.mitre.org/data/definitions/544.html>`_.

    :param py_dest: Path to a Python script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        py_dest=py_dest,
        exceptions_list=[
            'MemoryError',
        ],
        msgs={
            OPEN: 'Code declares a "catch" for MemoryError exceptions',
            CLOSED: 'Code does not declare "catch" for MemoryError exceptions',
        },
        exclude=exclude)


@api(risk=LOW, kind=SAST)
def uses_catch_for_syntax_errors(py_dest: str, exclude: list = None) -> tuple:
    """
    Search for the use of SyntaxError catch and its derived classes in a path.

    See `CWE-544 <https://cwe.mitre.org/data/definitions/544.html>`_.

    :param py_dest: Path to a Python script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        py_dest=py_dest,
        exceptions_list=[
            'TabError',
            'SyntaxError',
            'IndentationError',
        ],
        msgs={
            OPEN: 'Code declares catch for syntax error exceptions',
            CLOSED: 'Code does not declare catch for syntax error exceptions',
        },
        exclude=exclude)


@api(risk=LOW, kind=SAST)
def swallows_exceptions(py_dest: str, exclude: list = None) -> tuple:
    """
    Search for swallowed exceptions.

    Identifies ``except`` blocks that are either empty
    or only contain comments or the ``pass`` statement.

    :param py_dest: Path to a Python script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = (Keyword('except') + SkipTo(LineEnd(), include=True) +
               indentedBlock(Keyword('pass'), indentStack=[1]))
    grammar.ignore(pythonStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=py_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code has empty "catches"',
            CLOSED: 'Code does not have empty "catches"'
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=HIGH, kind=SAST)
def uses_insecure_functions(py_dest: str, exclude: list = None) -> tuple:
    """
    Search for insecure functions in code.

    Powered by Bandit.

    :param py_dest: Path to a Python script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(py_dest):
        return UNKNOWN, 'File does not exist'

    exclude = tuple(exclude) if exclude else tuple()
    results = list(filter(None.__ne__,
                          map(_insecure_functions_in_file,
                              get_paths(py_dest,
                                        endswith=LANGUAGE_SPECS['extensions'],
                                        exclude=exclude))))

    if results:
        return OPEN, 'Insecure functions were found in code', results
    return CLOSED, 'No insecure functions were found in code'
