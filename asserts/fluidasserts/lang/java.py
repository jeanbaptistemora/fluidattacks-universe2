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


def _declares_throws_for_exceptions(
    java_dest: str,
    exceptions_list: list,
    msgs: Dict[str, str],
    exclude: list = None,
) -> tuple:
    """Search for the declaration of throws for the given exceptions."""
    any_exception = L_VAR_CHAIN_NAME
    provided_exception = MatchFirst(
        [Keyword(exception) for exception in exceptions_list]
    )

    exception_group = delimitedList(expr=any_exception)
    exception_group.addCondition(
        # Ensure that at least one exception in the group is the provided one
        lambda tokens: any(provided_exception.matches(tok) for tok in tokens)
    )

    grammar = (
        Suppress(Keyword("throws") | Keyword("throw"))
        + exception_group
        + Suppress(Optional(L_VAR_NAME))
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
def uses_catch_for_null_pointer_exception(
    java_dest: str, exclude: list = None
) -> tuple:
    """
    Search for the use of NullPointerException "catch" in a path.

    See `CWE-395 <https://cwe.mitre.org/data/definitions/395.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        java_dest=java_dest,
        exceptions_list=[
            "NullPointerException",
            "lang.NullPointerException",
            "java.lang.NullPointerException",
        ],
        msgs={
            OPEN: (
                "Code uses NullPointerException "
                "Catch to Detect NULL Pointer Dereference"
            ),
            CLOSED: (
                "Code does not use NullPointerException "
                "Catch to Detect NULL Pointer Dereference"
            ),
        },
        exclude=exclude,
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


def _uses_insecure_cipher(
    java_dest: str, algorithm: tuple, exclude: list = None
) -> bool:
    """Check if code uses an insecure cipher algorithm."""
    method = 'Cipher.getInstance("{}")'.format(algorithm.upper())
    op_mode = "/" + oneOf("CBC ECB", caseless=True)
    padding = "/" + oneOf("NoPadding PKCS5Padding", caseless=True)
    algorithm = (
        '"'
        + CaselessKeyword(algorithm)
        + Optional(op_mode + Optional(padding))
        + '"'
    )

    grammar = (
        Suppress(Keyword("Cipher") + "." + Keyword("getInstance"))
        + nestedExpr()
    )
    grammar.ignore(javaStyleComment)
    grammar.addCondition(
        # Ensure that at least one token is the provided algorithm
        lambda tokens: tokens.asList()
        and any(algorithm.matches(tok) for tok in tokens[0])
    )

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: f"Code uses {method} method",
            CLOSED: f"Code does not use {method} method",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


def _uses_insecure_hash(
    java_dest: str, algorithm: tuple, exclude: list = None
) -> bool:
    """Check if code uses an insecure hashing algorithm."""
    method = f'MessageDigest.getInstance("{algorithm.upper()}")'
    tk_mess_dig = CaselessKeyword("messagedigest")
    tk_get_inst = CaselessKeyword("getinstance")
    tk_alg = Literal('"') + CaselessKeyword(algorithm.lower()) + Literal('"')
    tk_params = Literal("(") + tk_alg + Literal(")")
    grammar = tk_mess_dig + Literal(".") + tk_get_inst + tk_params
    grammar.ignore(javaStyleComment)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: f"Code uses {method} method",
            CLOSED: f"Code does not use {method} method",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(risk=MEDIUM, kind=SAST)
def uses_insecure_cipher(
    java_dest: str, algorithm: str, exclude: list = None
) -> bool:
    """
    Check if code uses an insecure cipher algorithm.

    See `REQ.148 <https://fluidattacks.com/products/rules/list/148/>`_.
    See `REQ.149 <https://fluidattacks.com/products/rules/list/149/>`_.

    :param java_dest: Path to a Java source file or package.
    :param algorithm: Insecure algorithm.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_cipher(java_dest, algorithm, exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_insecure_hash(
    java_dest: str, algorithm: str, exclude: list = None
) -> bool:
    """
    Check if code uses an insecure hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/products/rules/list/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param algorithm: Insecure algorithm.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_hash(java_dest, algorithm, exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_md5_hash(java_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses MD5 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/products/rules/list/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_hash(java_dest, "md5", exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_sha1_hash(java_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses MD5 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/products/rules/list/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_hash(java_dest, "sha-1", exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_des_algorithm(java_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses DES as encryption algorithm.

    See `REQ.149 <https://fluidattacks.com/products/rules/list/149/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_cipher(java_dest, "DES", exclude)


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


@api(risk=LOW, kind=SAST)
def uses_system_exit(java_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``System.exit`` calls in a  or package.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    method = "System.exit"
    grammar = Keyword("System") + "." + Keyword("exit")
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: f"Code uses {method} method",
            CLOSED: f"Code does not use {method} method",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(
    risk=MEDIUM,
    kind=SAST,
    standards={
        "CWE": "780",
    },
)
def uses_insecure_rsa(java_dest: str, exclude: list = None) -> tuple:
    """
    Check if RSA algorithm uses an insecure padding.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    :returns: - ``UNKNOWN`` on errors.
        - ``OPEN`` if an **OAEP** padding is not used or **ECB** mode is used.
        - ``CLOSED`` otherwise.

    """
    insecure_modes = "/" + oneOf("ECB", caseless=True)
    any_modes = "/" + Word(alphanums)

    padding = "/" + Word(alphanums + "-")
    padding.addCondition(lambda tokens: "oaep" not in str(tokens).lower())
    any_padding = "/" + Word(alphanums + "-")

    algorithm = (
        '"'
        + CaselessKeyword("RSA")
        + Optional((insecure_modes + any_padding) | (any_modes + padding))
        + '"'
    )

    grammar = (
        Suppress(Keyword("Cipher") + "." + Keyword("getInstance"))
        + nestedExpr()
    )
    grammar.ignore(javaStyleComment)
    grammar.addCondition(
        # Ensure that at least one token is the RSA algorithm
        lambda tokens: tokens.asList()
        and any(algorithm.matches(tok) for tok in tokens[0])
    )

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: (
                f"Code uses an insecure RSA padding scheme, "
                "OAEP padding is required"
            ),
            CLOSED: f"Code uses a secure RSA padding",
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
