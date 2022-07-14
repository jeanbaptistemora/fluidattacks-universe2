# -*- coding: utf-8 -*-

"""This module allows to check ``C#`` code vulnerabilities."""


from fluidasserts import (
    CLOSED,
    LOW,
    MEDIUM,
    OPEN,
    SAST,
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
    cppStyleComment,
    delimitedList,
    Empty,
    Keyword,
    MatchFirst,
    nestedExpr,
    Optional,
    QuotedString,
    Suppress,
    Word,
)
from typing import (
    Dict,
    List,
)

LANGUAGE_SPECS = {
    "extensions": ("cs",),
    "block_comment_start": "/*",
    "block_comment_end": "*/",
    "line_comment": ("//",),
}  # type: dict


# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')
# _Var_123
L_VAR_NAME = Word(alphas + "_", alphanums + "_")
# Class_123.property1.property1.value
L_VAR_CHAIN_NAME = delimitedList(L_VAR_NAME, delim=".", combine=True)


def _declares_catch_for_exceptions(
    csharp_dest: str,
    exceptions_list: List[str],
    msgs: Dict[str, str],
    allow_empty: bool = False,
    exclude: list = None,
) -> tuple:
    """Search for the declaration of catch for the given exceptions."""
    provided_exception = MatchFirst(
        [Keyword(exception) for exception in exceptions_list]
    )

    grammar = Keyword("catch") + nestedExpr(
        opener="(",
        closer=")",
        content=(provided_exception + Optional(L_VAR_NAME)),
    )
    if allow_empty:
        grammar = MatchFirst(
            [
                Keyword("catch") + nestedExpr(opener="{", closer="}"),
                grammar.copy(),
            ]
        )

    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs=msgs,
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(risk=LOW, kind=SAST)
def has_generic_exceptions(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Search for generic exceptions in a C# source file or package.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        csharp_dest=csharp_dest,
        exceptions_list=[
            "Exception",
            "ApplicationException",
            "SystemException",
            "System.Exception",
            "System.ApplicationException",
            "System.SystemException",
        ],
        allow_empty=True,
        msgs={
            OPEN: 'Code declares a "catch" for generic exceptions',
            CLOSED: 'Code does not declare "catch" for generic exceptions',
        },
        exclude=exclude,
    )


@api(risk=LOW, kind=SAST)
def uses_catch_for_null_reference_exception(
    csharp_dest: str, exclude: list = None
) -> tuple:
    """
    Search for the use of NullReferenceException "catch" in a path.

    See `CWE-395 <https://cwe.mitre.org/data/definitions/395.html>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        csharp_dest=csharp_dest,
        exceptions_list=[
            "NullReferenceException",
            "system.NullReferenceException",
        ],
        msgs={
            OPEN: (
                "Code uses NullReferenceException "
                "Catch to handle NULL Pointer Dereferences"
            ),
            CLOSED: (
                "Code does not use NullPointerException "
                "Catch to handle NULL Pointer Dereferences"
            ),
        },
        exclude=exclude,
    )


@api(risk=LOW, kind=SAST)
def swallows_exceptions(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``catch`` blocks that are empty or only have comments.

    See `REQ.161 <https://fluidattacks.com/products/rules/list/161/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    grammar = (
        Suppress(Keyword("catch"))
        + Optional(nestedExpr(opener="(", closer=")"))
        + nestedExpr(opener="{", closer="}", content=~Empty())
    )
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code has empty "catch" blocks',
            CLOSED: 'Code does not have empty "catch" blocks',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(risk=LOW, kind=SAST)
def has_switch_without_default(
    csharp_dest: str, exclude: list = None
) -> tuple:
    r"""
    Check if all ``switch``\ es have a ``default`` clause.

    See `REQ.161 <https://fluidattacks.com/products/rules/list/161/>`_.

    See `CWE-478 <https://cwe.mitre.org/data/definitions/478.html>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return core.generic_c_has_switch_without_default(
        csharp_dest, LANGUAGE_SPECS, exclude
    )


@api(risk=LOW, kind=SAST)
def has_insecure_randoms(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Check if code instantiates ``Random`` class.

    See `REQ.224 <https://fluidattacks.com/products/rules/list/224/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    # module: System
    # secure versions: System.Security.Cryptography.RandomNumberGenerator
    #                  System.Security.Cryptography.RNGCryptoServiceProvider
    grammar = (
        Keyword("new")
        + Optional(Keyword("System") + ".")
        + Keyword("Random")
        + nestedExpr()
    )
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: "Code generates insecure random numbers",
            CLOSED: "Code does not generate insecure random numbers",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(risk=LOW, kind=SAST)
def uses_debug_writeline(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses Debug.WriteLine method.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    methods = (
        "Write",
        "WriteIf",
        "WriteLine",
        "WriteLineIf",
        "Assert",
        "Fail",
        "Print",
    )
    grammar = Keyword("Debug") + "." + MatchFirst(map(Keyword, methods))
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: "Code uses Debug.WriteLine method",
            CLOSED: "Code does not use Debug.WriteLine method",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )
