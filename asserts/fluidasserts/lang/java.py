# -*- coding: utf-8 -*-

"""This module allows to check Java code vulnerabilities."""


from fluidasserts import (
    CLOSED,
    LOW,
    MEDIUM,
    OPEN,
    SAST,
    UNKNOWN,
)
from fluidasserts.helper import (
    lang,
)
from fluidasserts.lang import (
    core,
)
from fluidasserts.utils.decorators import (
    api,
)
from pyparsing import (
    alphanums,
    alphas,
    CaselessKeyword,
    delimitedList,
    Empty,
    javaStyleComment,
    Keyword,
    Literal,
    MatchFirst,
    nestedExpr,
    nums,
    oneOf,
    Optional,
    Or,
    QuotedString,
    Regex,
    Suppress,
    Word,
)
import re
from typing import (
    Dict,
    List,
)

LANGUAGE_SPECS = {
    "extensions": ("java",),
    "block_comment_start": "/*",
    "block_comment_end": "*/",
    "line_comment": ("//",),
}  # type: dict


# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')
# Var$_123
L_VAR_NAME = Word(alphas + "$_", alphanums + "$_")
# Class$_123.property1.property1.value
L_VAR_CHAIN_NAME = delimitedList(L_VAR_NAME, delim=".", combine=True)


def _declares_catch_for_exceptions(
    java_dest: str,
    exceptions_list: list,
    msgs: Dict[str, str],
    exclude: list = None,
) -> tuple:
    """Search for the declaration of catch for the given exceptions."""
    any_exception = L_VAR_CHAIN_NAME
    provided_exception = MatchFirst(
        [Keyword(exception) for exception in exceptions_list]
    )

    exception_group = delimitedList(expr=any_exception, delim="|")
    exception_group.addCondition(
        # Ensure that at least one exception in the group is the provided one
        lambda tokens: any(provided_exception.matches(tok) for tok in tokens)
    )

    grammar = Suppress(Keyword("catch")) + nestedExpr(
        opener="(",
        closer=")",
        content=(exception_group + Suppress(Optional(L_VAR_NAME))),
    )
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs=msgs,
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(risk=LOW, kind=SAST)
def has_insecure_randoms(java_dest: str, exclude: list = None) -> tuple:
    r"""
    Check if code uses insecure random generators.

    - ``java.util.Random()``.
    - ``java.lang.Math.random()``.

    See `REQ.224 <https://fluidattacks.com/products/rules/list/224/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    _java = Keyword("java")
    _util = Keyword("util")
    _lang = Keyword("lang")
    _math = Keyword("Math")
    _import = Keyword("import")
    _random_minus = Keyword("random")
    _random_mayus = Keyword("Random")
    _args = nestedExpr()

    grammar = MatchFirst(
        [
            # util.Random()
            _util + "." + _random_mayus + _args,
            # Math.random()
            _math + "." + _random_minus + _args,
            # import java.util.Random
            _import + _java + "." + _util + "." + _random_mayus,
            # import java.lang.Math.random
            _import + _java + "." + _lang + "." + _math + "." + _random_minus,
        ]
    )
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: "Code uses insecure random generators",
            CLOSED: "Code does not use insecure random generators",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(risk=LOW, kind=SAST)
def has_log_injection(java_dest: str, exclude: list = None) -> tuple:
    """
    Search code injection.

    Check if the code does not neutralize or incorrectly neutralizes
    output that is written to logs.

    See `CWE-117 <https://cwe.mitre.org/data/definitions/117.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    log_variable = CaselessKeyword("log")
    log_level = oneOf("trace debug info warn error fatal")

    log_object = log_variable + Literal(".") + log_level

    tk_string = QuotedString('"')
    tk_var = Word(alphanums)

    grammar = log_object + Literal("(") + tk_string + Literal("+") + tk_var
    grammar.ignore(javaStyleComment)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: "Code allows logs injection",
            CLOSED: "Code does not allow logs injection",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(
    risk=MEDIUM,
    kind=SAST,
)
def uses_various_verbs_in_request_mapping(
    java_dest: str, exclude: list = None
):
    """
    Check if code uses various HTTP verbs in a RequestMapping.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    verbs_list = [
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "CONNECT",
        "OPTIONS",
        "TRACE",
        "PATCH",
    ]

    def any_content(limit):
        return Suppress(Regex(rf"(.*?{limit})+", flags=re.DOTALL))

    only_verb = Word(alphas) + Suppress(Optional(Literal(",")))

    req_verb = (
        Suppress(Keyword("RequestMethod") + ".")
        + Word(alphas)
        + Suppress(Optional(Literal(",")))
    )

    verbs = Or([only_verb, req_verb])

    methods = Suppress("=") + nestedExpr(opener="{", closer="}", content=verbs)

    content = any_content("method") + methods
    grammar = Suppress(Keyword("@RequestMapping")) + nestedExpr(
        content=content
    )

    grammar.ignore(javaStyleComment)

    def flatten(elements, aux_list=None):
        aux_list = aux_list if aux_list is not None else []
        for i in elements:
            if isinstance(i, list):
                flatten(i, aux_list)
            else:
                aux_list.append(i)
        return aux_list

    def count_verbs(k):
        count = 0
        data = flatten(k.asList())
        for i in data:
            if i in verbs_list:
                count += 1
        return count > 1

    grammar.addCondition(count_verbs)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: "Code uses uses various HTTP verbs in a RequestMapping",
            CLOSED: "Code uses only HTTP verbs per RequestMapping",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )
