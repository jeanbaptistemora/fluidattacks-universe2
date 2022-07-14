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


@api(risk=LOW, kind=SAST, standars={"CWE": "397"})
def throws_generic_exceptions(java_dest: str, exclude: list = None):
    """
    Check if the code throws generic exceptions.

    Throwing overly broad exceptions promotes complex error handling code that
    is more likely to contain security vulnerabilities.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_throws_for_exceptions(
        java_dest=java_dest,
        exceptions_list=[
            "Exception",
            "Throwable",
            "lang.Exception",
            "lang.Throwable",
            "java.lang.Exception",
            "java.lang.Throwable",
        ],
        msgs={
            OPEN: "Code throws generic exceptions",
            CLOSED: "Code does not throw generic exceptions",
        },
        exclude=exclude,
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
def uses_catch_for_runtime_exception(
    java_dest: str, exclude: list = None
) -> tuple:
    """
    Search for the use of RuntimeException "catch" in a path.

    See `CWE-544 <https://cwe.mitre.org/data/definitions/544.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        java_dest=java_dest,
        exceptions_list=[
            "RuntimeException",
            "lang.RuntimeException",
            "java.lang.RuntimeException",
        ],
        msgs={
            OPEN: (
                "Code declares a catch for RuntimeException "
                "to handle programming mistakes "
                "instead of prevent them by coding defensively"
            ),
            CLOSED: "Code does not declare a catch for RuntimeException",
        },
        exclude=exclude,
    )


@api(risk=LOW, kind=SAST)
def uses_print_stack_trace(java_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``printStackTrace`` calls in a path.

    See `CWE-209 <https://cwe.mitre.org/data/definitions/209.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = "." + Keyword("printStackTrace")
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: "Code uses Throwable.printStackTrace() method",
            CLOSED: "Code does not use Throwable.printStackTrace() method",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(risk=LOW, kind=SAST)
def does_not_handle_exceptions(
    java_dest: str,
    should_have: List[str],
    use_regex: bool = False,
    exclude: List[str] = None,
) -> tuple:
    """
    Search for ``catch`` blocks that do not handle the exception.

    See `REQ.161 <https://fluidattacks.com/products/rules/list/161/>`_.

    See `CWE-755 <https://cwe.mitre.org/data/definitions/755.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param should_have: List of expected exception handlers.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    if not use_regex:
        should_have = list(map(re.escape, should_have))
    should_have_regexps = tuple(re.compile(sh) for sh in should_have)

    grammar = Suppress(
        Keyword("catch") + nestedExpr(opener="(", closer=")")
    ) + nestedExpr(opener="{", closer="}")
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_CHAR)
    grammar.ignore(L_STRING)
    grammar.addCondition(
        lambda x: not any(shr.search(str(x)) for shr in should_have_regexps)
    )

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code has "catch" blocks that do not handle its exceptions',
            CLOSED: 'All "catch" blocks in code handles its exceptions',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(risk=LOW, kind=SAST)
def has_switch_without_default(java_dest: str, exclude: list = None) -> tuple:
    r"""
    Check if all ``switch``\ es have a ``default`` clause.

    See `REQ.161 <https://fluidattacks.com/products/rules/list/161/>`_.

    See `CWE-478 <https://cwe.mitre.org/data/definitions/478.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return core.generic_c_has_switch_without_default(
        java_dest, LANGUAGE_SPECS, exclude
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
def has_if_without_else(
    java_dest: str,
    conditions: list,
    use_regex: bool = False,
    exclude: list = None,
) -> tuple:
    r"""
    Check if all ``if``\ s have an ``else`` clause.

    See `REQ.161 <https://fluidattacks.com/products/rules/list/161/>`_.

    :param java_dest: Path to a Java source file or package.
    :param conditions: List of texts between parentheses of the
                      `if (condition)` statement.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return core.generic_c_has_if_without_else(
        java_dest, conditions, use_regex, LANGUAGE_SPECS, exclude
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


@api(risk=MEDIUM, kind=SAST)
def uses_insecure_aes(java_dest: str, exclude: list = None):
    """
    Check if code uses an insecure AES mode.

    AES should not be used with ECB or CBC/PKCS5Padding.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    ecb_mode = "/" + CaselessKeyword("ECB")
    cbc_mode = "/" + CaselessKeyword("CBC")
    padding_pkc = "/" + CaselessKeyword("PKCS5Padding")
    padding_all = "/" + Word(alphanums)
    algorithm = (
        '"'
        + CaselessKeyword("AES")
        + Optional(((ecb_mode + padding_all) | (cbc_mode + padding_pkc)))
        + '"'
    )

    grammar = (
        Suppress(Keyword("Cipher") + "." + Keyword("getInstance"))
        + nestedExpr()
    )
    grammar.ignore(javaStyleComment)
    grammar.addCondition(
        # Ensure that at least one token is the AES algorithm
        lambda tokens: tokens.asList()
        and any(algorithm.matches(tok) for tok in tokens[0])
    )

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: f"Code uses insecure AES modes",
            CLOSED: f"Code uses secure AES modes",
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
def uses_cipher_in_ecb_mode(java_dest: str, exclude: list = None):
    """
    Check if ECB cipher mode is being used.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    insecure_modes = "/" + oneOf("ECB", caseless=True)
    any_padding = "/" + Word(alphanums + "-")
    any_algorithm = Word(alphanums)

    algorithm = '"' + any_algorithm + insecure_modes + any_padding + '"'
    grammar = (
        Suppress(Keyword("Cipher") + "." + Keyword("getInstance"))
        + nestedExpr()
    )
    grammar.ignore(javaStyleComment)
    grammar.addCondition(
        # Ensure that at least one token is the ECB mode
        lambda tokens: tokens.asList()
        and any(algorithm.matches(tok) for tok in tokens[0])
    )

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: f"Code uses an insecure cipher mode (ECB)",
            CLOSED: f"Code uses a secure cipher mode",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(
    risk=MEDIUM,
    kind=SAST,
)
def uses_broken_password_encryption(java_dest: str, exclude: list = None):
    """
    Check if code use insecure methods to encrypt passwords.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    _import_security = Keyword("org.springframework.security")
    insecure_inports = [
        ".authentication.encoding.Md5PasswordEncoder",
        ".authentication.encoding.ShaPasswordEncoder",
        ".crypto.password.LdapShaPasswordEncoder",
        ".crypto.password.Md4PasswordEncoder",
        ".crypto.password.MessageDigestPasswordEncoder",
        ".crypto.password.NoOpPasswordEncoder",
        ".crypto.password.StandardPasswordEncoder",
        ".crypto.scrypt.SCryptPasswordEncoder",
    ]

    grammar = MatchFirst([_import_security + i for i in insecure_inports])
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: "Code uses insecure methods to cipher passwords",
            CLOSED: "Code uses secure methods to cipher passwords",
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )


@api(
    risk=MEDIUM,
    kind=SAST,
)
def uses_insecure_ssl_context(java_dest: str, exclude: list = None):
    """
    Check if code uses insecure SSL context.

    The secure versions are:
        - TLS.
        - DTLS.
        - TLSv1.2.
        - DTLSv1.2.
        - TLSv1.3.
        - DTLSv1.3.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    secure_versions = MatchFirst(
        [
            CaselessKeyword(i)
            for i in [
                '"TLS"',
                '"DTLS"',
                '"TLSv1.2"',
                '"DTLSv1.2"',
                '"TLSv1.3"',
                '"DTLSv1.3"',
            ]
        ]
    )
    grammar = (
        Suppress(Keyword("SSLContext") + "." + Keyword("getInstance"))
        + nestedExpr()
    )
    grammar.ignore(javaStyleComment)
    grammar.addCondition(
        # Ensure the matching token is not one of the secure algorithms
        lambda tokens: tokens.asList()
        and not any(secure_versions.matches(tok) for tok in tokens[0])
    )
    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: "Code uses insecure SSL context version",
            CLOSED: "Code uses secure SSL context version",
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


@api(
    risk=MEDIUM,
    kind=SAST,
)
def uses_insecure_key_pair_length(java_dest: str, exclude: list = None):
    """
    Check if the code uses an insecure length to generate key pairs.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    algorithm = nestedExpr(
        content=Suppress('"') + Word(alphas) + Suppress('"')
    )("alg_name")

    length = Suppress(Keyword("init")) + nestedExpr(content=Word(nums))

    def check_length(tokens):
        alg_name = tokens.alg_name[0][0].replace('"', "").lower()
        alg_length = int(tokens.alg_length)
        must_lengts = {
            "rsa": 4096,
            "dsa": 3000,
            "ec": 270,
            "diffiehellman": 512,
        }
        try:
            return alg_length < must_lengts[alg_name]
        except KeyError:
            return UNKNOWN, f"{alg_name} algorithm cannot be recognized."

    anything_except_get_instance = Regex(r"(.*?;)+", flags=re.DOTALL)

    instance = Suppress(
        "=" + Keyword("KeyPairGenerator") + "." + Keyword("getInstance")
    )

    grammar = (
        L_VAR_NAME.copy()("varname1")
        + instance
        + algorithm
        + anything_except_get_instance("regex")
    )

    def flatten(elements, aux_list=None):
        aux_list = aux_list if aux_list is not None else []
        for i in elements:
            if isinstance(i, list):
                flatten(i, aux_list)
            else:
                aux_list.append(i)
        return aux_list

    def set_length(tokens):
        gramm = tokens.varname1 + Suppress(".") + length("alg_length")
        gramm.ignore(javaStyleComment)
        data1 = flatten(gramm.searchString(tokens.regex).asList())
        setattr(tokens, "varname2", data1[0])
        setattr(tokens, "alg_length", data1[1])

    grammar.ignore(javaStyleComment)
    grammar.setParseAction(set_length)
    grammar.addCondition(check_length)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: (
                "The code uses an insecure length for the "
                "algorithm that generates the key pairs."
            ),
            CLOSED: (
                "The code uses a secure length for the "
                "algorithm that generates the key pairs."
            ),
        },
        spec=LANGUAGE_SPECS,
        excl=exclude,
    )
