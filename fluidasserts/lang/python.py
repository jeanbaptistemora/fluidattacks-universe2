# -*- coding: utf-8 -*-

"""This module allows to check Python code vulnerabilities."""

# standard imports
import os

# 3rd party imports
from bandit import blacklists
from pyparsing import (CaselessKeyword, Word, Literal, Optional, alphas,
                       pythonStyleComment, Suppress, delimitedList, Forward,
                       SkipTo, LineEnd, indentedBlock, Group)

# local imports
from fluidasserts.helper import lang
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.decorators import track, level, notify


LANGUAGE_SPECS = {
    'extensions': ('py',),
    'block_comment_start': None,
    'block_comment_end': None,
    'line_comment': ('#',)
}  # type: dict


def _call_in_code(call, code_content):
    """Check if call is present in code_file."""
    import ast

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
    import ast

    code_tree = ast.parse(code_content)
    for node in code_tree.body:
        if isinstance(node, ast.Import):
            for name in node.names:
                if import_name == name.name:
                    return True
    return False


def _insecure_functions_in_file(py_dest: str) -> bool:
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

    return {py_dest: results} if results else None


def _get_block(file_lines, line) -> str:
    """
    Return a Python block of code beginning in line.

    :param file_lines: Lines of code
    :param line: First line of block
    """
    frst_ln = file_lines[line - 1]
    file_lines = file_lines[line - 1:]
    rem_file = "\n".join(file_lines)
    indent_stack = [len(frst_ln) - len(frst_ln.lstrip(' ')) + 1]
    prs_block = Forward()
    block_line = SkipTo(LineEnd())
    block_header = SkipTo(LineEnd())
    block_body = indentedBlock(prs_block, indent_stack)
    block_def = Group(block_header + block_body)
    # pylint: disable=pointless-statement
    prs_block << (block_def | block_line)
    block_list = prs_block.parseString(rem_file).asList()
    block_str = (lang.lists_as_string(block_list, '', 0))
    return block_str.rstrip()


@notify
@level('low')
@track
def has_generic_exceptions(py_dest: str, exclude: list = None) -> bool:
    """
    Search for generic exceptions in a Python script or package.

    :param py_dest: Path to a Python script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    tk_except = CaselessKeyword('except')
    generic_exception = tk_except + Literal(':')

    result = False
    try:
        matches = lang.check_grammar(generic_exception, py_dest,
                                     LANGUAGE_SPECS, exclude)
        if not matches:
            show_close('Code does not use generic exceptions',
                       details=dict(code_dest=py_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist', details=dict(code_dest=py_dest))
        return False
    else:
        result = True
        show_open('Code uses generic exceptions',
                  details=dict(file=matches,
                               total_vulns=len(matches)))
    return result


@notify
@level('low')
@track
def swallows_exceptions(py_dest: str, exclude: list = None) -> bool:
    """
    Search for swallowed exceptions.

    Identifies ``except`` blocks that are either empty
    or only contain comments or the ``pass`` statement.

    :param py_dest: Path to a Python script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    tk_except = CaselessKeyword('except')
    tk_word = Word(alphas) + Optional('.')
    tk_pass = Literal('pass')
    tk_exc_obj = tk_word + Optional(Literal('as') + tk_word)
    parser_exception = tk_except + \
        Optional('(') + \
        Optional(delimitedList(tk_exc_obj)) + \
        Optional(')') + Literal(':')
    empty_exception = (Suppress(parser_exception) +
                       tk_pass).ignore(pythonStyleComment)

    result = False
    try:
        matches = lang.check_grammar(parser_exception, py_dest,
                                     LANGUAGE_SPECS, exclude)
        if not matches:
            show_close('Code does not have excepts',
                       details=dict(code_dest=py_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist', details=dict(code_dest=py_dest))
        return False
    vulns = {}
    for code_file, val in matches.items():
        vulns.update(lang.block_contains_grammar(empty_exception, code_file,
                                                 val['lines'], _get_block))
    if not vulns:
        show_close('Code does not have empty "catches"',
                   details=dict(file=py_dest,
                                fingerprint=get_sha256(py_dest)))
    else:
        show_open('Code has empty "catches"',
                  details=dict(matched=vulns,
                               total_vulns=len(vulns)))
        result = True
    return result


@notify
@level('high')
@track
def uses_insecure_functions(py_dest: str, exclude: list = None) -> bool:
    """
    Search for insecure functions in code.

    Powered by Bandit.

    :param py_dest: Path to a Python script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    if not os.path.exists(py_dest):
        show_unknown('File does not exist', details=dict(code_dest=py_dest))
        return False

    exclude = tuple(exclude) if exclude else tuple()
    results = tuple(filter(None.__ne__,
                           map(_insecure_functions_in_file,
                               get_paths(py_dest,
                                         endswith=LANGUAGE_SPECS['extensions'],
                                         exclude=exclude))))

    if results:
        show_open('Insecure functions were found in code',
                  details=dict(matched=results))
        return True
    show_close('No insecure functions were found in code',
               details=dict(location=py_dest))
    return False
