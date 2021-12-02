---
slug: parse-conquer/
title: Parse and Conquer
date: 2019-05-07
subtitle: Why Asserts uses Parser combinators
category: attacks
tags: software, security, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330971/blog/parse-conquer/cover_avf8fy.webp
alt: Photo by Markus Spiske on Unsplash
description: 'For this blog post, we rely on the following question:
  Why does Asserts use parser combinators as
  its main static code analysis tool?'
keywords: Parsing, Asserts, Combinators, Regex, Vulnerability, Pyparsing,
  Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/qjnAnF0jIGk
---

As you might have noticed at `Fluid Attacks` we like [parser
combinators](../pars-orationis-secura/), [functional
programming](../why-we-go-functional), and of course,
[Python](../tags/python/). In the parser article, we showed you the
essentials of `Pyparsing` and we also showed how to leverage its power
to find `SQL` injections in a `PHP` application. Here we will extend
those essentials to show you how we used parser combinators in Asserts,
our vulnerability closure checker engine (considering that we not longer
support this product). Feel free to refer to that article for more
details on how `Pyparsing` works, though I’ll try my best to explain
every keyword used here.

Parser combinators are particularly useful analyzing complex
expressions. You don’t really need parser combinators to break up email
addresses into usernames and domains. For that, a regular expression
will suffice. However, when what you need to do is more involved, such
as looking for `SQL` injections or analyzing source code for poor
programming practices per our
[**Criteria**](https://docs.fluidattacks.com/criteria/) and
recommendations, then parsers are our tool of choice. This is one of the
tasks at which `Asserts` excels. Determine whether a vulnerability that
has been found in the source code by one of our analysts is still open
by doing a deep search within it with the aid of parser combinators.
Let’s see how that works.

Suppose an analyst was auditing some `Java` source code and found out
that it uses the insecure `DES` cipher to mask the information of a bank
transaction in the file `transactions.java`. `DES` is insecure due to
its small 56-bit key size which could theoretically be brute-forced in 6
minutes. In order to report the vulnerability, they could write a script
that automatically checks if the vulnerability is still there.

**Asserts script `expl.py` to check DES usage.**

``` python
from fluidasserts.lang import java

FILE = 'transactions.java'
java.uses_des_algorithm(FILE)
```

Simple, right? Just running that script tells you whether or not the
insecure `DES` algorithm is used in that particular file. Or you can
even point it at an entire directory and `Asserts` will test every
`Java` source file for `DES` usage. But what’s behind the curtain? Since
`Asserts` is now open-source, anyone can actually check out what this
function does.

**java.py. See
[Gitlab](https://gitlab.com/fluidattacks/asserts/blob/master/fluidasserts/lang/java.py#L395)
for rest of code.**

``` python
from pyparsing import (CaselessKeyword, Word, Literal, Optional, alphas, Or,
                       alphanums, Suppress, nestedExpr, javaStyleComment,
                       SkipTo, QuotedString, oneOf)

from fluidasserts.helper import lang

...

def uses_des_algorithm(java_dest: str, exclude: list = None) -> bool:
    """
    Check if code uses DES as encryption algorithm.

    See `https://docs.fluidattacks.com/criteria/cryptography/149`_.

    :param java_dest: Path to a Java source file or package.
    """
    method = 'Cipher.getInstance("DES")'
    tk_mess_dig = CaselessKeyword('cipher')
    tk_get_inst = CaselessKeyword('getinstance')
    tk_alg = Literal('"') ` CaselessKeyword('des') ` Literal('"')
    tk_params = Literal('(') ` tk_alg ` Literal(')')
    instance_des = tk_mess_dig ` Literal('.') ` tk_get_inst + tk_params

    result = False
    try:
        matches = lang.check_grammar(instance_des, java_dest, LANGUAGE_SPECS,
                                     exclude)
        if not matches:
            show_unknown('Not files matched',
                         details=dict(code_dest=java_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist', details=dict(code_dest=java_dest))
        return False
    for code_file, vulns in matches.items():
        if vulns:
            show_open('Code uses {} method'.format(method),
                      details=dict(file=code_file,
                                   fingerprint=lang.
                                   file_hash(code_file),
                                   lines=", ".join([str(x) for x in vulns]),
                                   total_vulns=len(vulns)))
            result = True
        else:
            show_close('Code does not use {} method'.format(method),
                       details=dict(file=code_file,
                                    fingerprint=lang.
                                    file_hash(code_file)))
    return result
```

Notice how, in the first few lines (17-22)above, the parser
`instance_des` is built from smaller parsers such as `tk_mess_dig`,
which matches the single keyword "Cipher", but also any variations in
case, should they happen. `CaselessKeyword`. `Literal` does not make any
such assumption: if its double quotes, they must be there. `Pyparsing`
also takes care of handling white space by overloading the `+` operator
to mean "followed possibly with some whitespace in between". Building a
regex to match the same thing would be perhaps more compact, but never
as readable or maintainable. This is one of the many advantages of
parser combinators over regular expressions.

Next, this parser is passed along with the other required parameters to
the function `check_grammar` in the `lang` module (more on that later).
This function should return the matches in said file for the built
parser. Thus the actual matching code can be reused. If there are
matches, that means the vulnerability is open, hence `Asserts` will
`show_open` a message like this:

<div class="imgblock">

!["Asserts open vulnerability message"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330969/blog/parse-conquer/asserts-open-msg_otjbo5.webp)

<div class="title">

Figure 1. Asserts open vulnerability message

</div>

</div>

Otherwise it shows a similar message, only with fewer alarming colors.

So, what does the `lang` module do with the combined parsers and the
file? More parsing. It tests whether the path is a single file or a
directory whether or not it has the correct extension, but really all
the most important stuff is in the `get_match_lines` method. It parses
the text in the given source code file to find out if those lines are
comments, i.e., not functional code, so as to skip them. In the future,
`Asserts` will be able to use this comment-code discrimination to find
lines of code which were commented out and later abandoned. This would
be important because these commented-out lines of code might exhibit
unpredictable behavior in the application if they were carelessly
uncommented, depending on who has access to the code.

**From `fluidasserts.helper.lang` module. See full code in
[Gitlab](https://gitlab.com/fluidattacks/asserts/blob/master/fluidasserts/helper/lang.py).**

``` python
def _get_match_lines(grammar: ParserElement, code_file: str,  # noqa
                     lang_spec: dict) -> List:  # noqa
    """
    Check grammar in file.

    :param grammar: Pyparsing grammar against which file will be checked.
    :param code_file: Source code file to check.
    :param lang_spec: Contains language-specific syntax elements, such as
                       acceptable file extensions and comment delimiters.
    :return: List of lines that contain grammar matches.
    """
    with open(code_file, encoding='latin-1') as file_fd:
        affected_lines = []
        counter = 0
        in_block_comment = False
        for line in file_fd.readlines():
            counter += 1
            try:
                if lang_spec.get('line_comment'):
                    parser = ~Or(lang_spec.get('line_comment'))
                    parser.parseString(line)
            except ParseException:
                continue
            if lang_spec.get('block_comment_start'):
                try:
                    block_start = Literal(lang_spec.get('block_comment_start'))
                    parser = SkipTo(block_start) + block_start
                    parser.parseString(line)
                    in_block_comment = True
                except (ParseException, IndexError):
                    pass

                if in_block_comment and lang_spec.get('block_comment_end'):
                    try:
                        block_end = Literal(lang_spec.get('block_comment_end'))
                        parser = SkipTo(block_end) + block_end
                        parser.parseString(line)
                        in_block_comment = False
                        continue
                    except ParseException:
                        continue
                    except IndexError:
                        pass
            try:
                results = grammar.searchString(line, maxMatches=1)
                if not _is_empty_result(results):
                    affected_lines.append(counter)
            except ParseException:
                pass
    return affected_lines
```

After testing if the code we’re looking at is functional or not, it is
simply a matter of invoking the `searchString` method from `PyParsing`,
which as its name implies, searches the given string for matches of the
given parser. The module has a few more tricks up its sleeve, such as
turning the parsing search results into pretty strings and parsing
chunks of lines of code. All that again with the help of parser
combinators.

The most important takeaway from looking at this single function’s
source code, and what lies behind it, is that using parser combinators
in `Asserts` allows us not only to have readable, maintainable code for
our own use and the use of others but also for this code to be easily
*extensible* and *reusable*. Due to its object-oriented interface, clear
naming conventions, and that coding parsers in it are just *pythonic*,
`PyParsing` allows our team to write and rewrite static code analysis
tools that will change along with its users' needs.

That wouldn’t be possible with regular expressions. Regexes must be
tailor-made, carefully designed with one specific objective in mind. One
application. So that regex that might search for conditionals without
default actions in `Javascript`, will be useless for the same purpose in
a different language. Such is not the case with parser combinators as
most code is easily modified or reusable. Also, nesting searches as we
did above (parsing before parsing to know if we’re inside a block
comment) will definitely require uber-complex regular expressions, if it
is possible at all.

Just like `uses_des_algorithm` above, `Asserts` packs convenient
functions to test for many of our requirements or recommendations for
secure coding, for several different languages, and growing daily.
`Pyparsing` enhances a significant part of our static code analysis
tools in a way that, as mentioned earlier, with regexes would only be
*ad hoc* or impossible to maintain.

## References

1. [`Asserts`](https://fluidattacks.gitlab.io/asserts/) documentation.

2. McGuire, Paul (2008). 'Getting Started with Pyparsing'. O’Reilly
    Short Cuts.
