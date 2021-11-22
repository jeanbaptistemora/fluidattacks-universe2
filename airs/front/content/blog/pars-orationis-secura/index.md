---
slug: pars-orationis-secura/
title: Pars Orationis Non Est Secura
date: 2018-03-22
subtitle: Using parser combinators to detect flaws
category: attacks
tags: detect, injection, scanner
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330971/blog/pars-orationis-secura/cover_gvmczz.webp
alt: Person holding sticky note
description: Learn here how to use Python and pyparsing to parse application
  code in order to find SQL injections in bWAPP.
keywords: Attack, Detection, Parser, Python, Injection, SQL, BWAPP,
  Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/D9Zow2REm8U
---

We like [`bWAPP`](http://itsecgames.com/) around here, because it’s
'very buggy\!'. We have shown here how to find and exploit
vulnerabilities like
[`SQL`](../fuzzy-bugs-online/#comparison-with-manual-injection)
[injection](../importance-pentesting/), [directory
traversal](../gherkin-steroids/#dynamic-detection-and-exploitation),
[`XPath`
injection](../xml-exploitable-markup-language/#injecting-xpath-into-a-vulnerable-app),
and [`UNIX` command
injection](../app-pickle/#documenting-attack-vectors). All of these have
one thing in common, namely: they could have been prevented with a
little [Input
Validation](https://www.owasp.org/index.php/Data_Validation).

Taking some ideas from [static code analysis](../exploit-code-graph/)
and the ['code-as-data'](../oracle-code/) approach, what if we could use
some sort of code or syntax analysis tool in order to gain intelligence
about where an apps’s weaknesses lie? That’s what we use 'parsers' for.

## Manual detection

Let us consider, for example, this site in our favorite buggy web app:

<div class="imgblock">

!["Add entry to blog screenshot"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330970/blog/pars-orationis-secura/add-entry_bmtgtk.webp)

<div class="title">

Figure 1. Adding an entry to the ``blog.''

</div>

</div>

Every time we load the page, the current entries in the blog are
`SELECTed` from a `MySQL` database.

The source code for such a page is like this:

**Adapted from `bWAPP`. Braces and loads of lines removed..**

``` php
<?php
include("functions_external.php"); // more includes
$entry = ""; // more variables
function sqli($data)
  $data = sqli_check_1($data); ... return $data;
?>
<html>...<header><h1>bWAPP</h1> <h2>an extremely buggy web app !</h2> </header>
<div id="menu">  ... </div> // other divs
<div id="main">
  <h1>SQL Injection - Stored (Blog)</h1>
  <form action="<?php echo($_SERVER["SCRIPT_NAME"]);?>" method="POST">
      <?php
        $entry = sqli($_POST["entry"]);
        $owner = $_SESSION["login"];
        $sql = "INSERT INTO blog (date, entry, owner) VALUES (now(),'" . $entry . "','" . $owner . "')";
        $recordset = $link->query($sql);
      ?>
  </form>
  <?php
    $sql = "SELECT * FROM blog";
    $recordset = $link->query($sql);
    while($row = $recordset->fetch_object())
       <tr height="40">
            <td align="center"> <?php echo $row->id; ?></td>
            <td><?php echo $row->owner; ?></td>
            <td><?php echo $row->date; ?></td>
            <td><?php echo xss_check_3($row->entry); ?></td>
        </tr>
  ?>
</div>
<div id="side">...</div> // other divs
</body></html>
```

We’re mainly interested in the `PHP` and `HTML` mixed in the `<div
id="main">`, which is just what we cropped here, because that’s where
the `SQL` is. Looking at a few more sources, we see we always exploit
the same weakness:

An `SQL` query is made up by 'concatenating' literal values, `PHP`
function calls and `PHP` variables like `$entry` above. That variable
comes from a `POST` request and passed through the sanitizing function
`SQLi`. After concatenating and building the query, it is sent to the
database for processing.

Thus we could type

``` sql
a','b'; drop table blog;--
```

into the entry field to turn the query into a dangerous, blog-deleting
one.

In order to successfully identify these `SQL` injections, we need to
look for strings which contain `SQL` code, and also use the `PHP`
concatenation (`first . last`). That’s not enough, because we also need
to relate the concatenated variable with the input or parameter where we
are going to place the malicious `SQL` code.

To hunt `SQL` injections in `bWAPP`, our tool of choice will be a set of
'parsers', i.e., a piece of software used to scan a string or file to
look for parts that conform to a specific set of rules.

## Specifying the targets

Before going into parsing and grammar issues, let us first reflect about
what we want to find. We want to detect pieces of text in the code that
conform to the syntax of an `SQL` `SELECT` or `INSERT` statement. But
also they must have concatenations, because a simple statement like

``` sql
SELECT * FROM blog;
```

is perfectly safe. Where could we possibly inject anything?

So we need `SELECT` or `INSERT` with concatenations. Also, we want our
tool to be able to identify

- which variable is at risk,

- where and how it is defined,

- whether or not it is protected by some function

For our purposes, the `INSERT` statement has this form:

``` sql
INSERT INTO tbl_name [column-names] VALUES (value-list)
```

We’ll use subparsers to define what each of these elements mean, v.g.,
values. But what is a value? Consider this rich example:

``` sql
INSERT INTO table VALUES ('1', NOW(), '" . $var1 . "','" . clean($var2, 1) . "'
```

A value can thus be:

- a fixed number or string,

- a `MySQL` function like `NOW()`,

- a concatenation of a string or number obtained from

    - a `PHP` variable (`$var1`) or

    - a `PHP` function (`clean()`), which may also take arguments.

This is where parsers shine and the alternative approach, [regular
expressions](https://en.wikipedia.org/wiki/Regular_expression), fail.
Imagine trying to write a `regex` to match such an `INSERT` with
concatenations. It would be humongous, not to mention very hard to
understand. Other disadvantages of regular expressions are that they
have to deal with white space explicitly and are hard to maintain when
there are any changes to the language syntax. As the famous saying goes:

> Some people, when confronted with a problem, think "I know, I’ll use
> regular expressions." Now they have two problems.
>
> —  Jamie Zawinski

## Learning the parser-tongue

Our weapon of choice will be `Python` and
[`pyparsing`](http://pyparsing.wikispaces.com/).

<div class="imgblock">

!["Comic about pyparsing and Harry Potter"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330971/blog/pars-orationis-secura/parsertongue_wzlpp5.webp)

<div class="title">

Figure 2. You don’t need to be a wizard to use `pyparsing`!

</div>

</div>

Some nice features about `pyparsing`:

- uses a simple syntax that makes the grammar transparent

- fits well in your `Python` code,

- uses standard class constructs and plain language instead of cryptic
  odd symbols,

- is tolerant to change and easy to adapt to different input or
  targets to match,

- includes a few nice helper functions, like parsing actions (v.g.
  convert a string of digits to an actual integer)

In `pyparsing`, the outermost parser for the `INSERT` above translates
to:

``` python
sql_insert = CaselessKeyword("INSERT INTO") ` sql_identifier ` Optional(column_names)
       ` CaselessKeyword("VALUES") ` values
```

The functions in `SentenceCase` are built into `pyparsing`, and their
names are pretty self-explanatory. The `+` operator is overloaded to
mean "followed by".

``` python
sql_identifier = Word(alphanums + "_")
values = Group( Literal("(") ` delimitedList(value) ` Literal(")") ).setResultsName("values")
```

Take `Word` to mean any combination of the given characters. Thus
`sql_identifier` is just a combination of alphanumeric characters and
the underscore. `values` is just a delimited list of values, enclosed in
parentheses. We `Group` that list into a single entity so that we may
refer to it by name later.

`PHP` identifiers are like `SQL` names, but **must** start with the
symbol `$`. We also define function calls:

``` python
php_identifier = Combine( Literal("$") + sql_identifier ).setResultsName("php identifier")
php_funcall = Combine( sql_identifier ` Literal("(") `
             ` Optional(delimitedList(php_identifier)) ` Literal(")") )
```

Unlike `Group`, `Combine` squashes all matched tokens into one. We do
that because we don’t really care about every single part of a function
call, only the `php_identifiers` inside, and we can access that by the
name with which we baptized `PHP` identifiers above.

Finally, we get to the heart of the matter: a `value` to be inserted is
either a literal word or number, the result of a function, or a
'dangerous concatenation':

``` python
value = varchar ^ php_funcall ^ danger_concat
danger = ( ... ` (php_identifier ^ php_funcall) ` ... ).setResultsName("danger identifier")
```

Here `^` is the logical connector `or`, and we’ve omitted a bunch of
`Literal` parsers for all the quotes and dots. By the way, notice that
all these named parts of our big parser are parsers themselves, and we
can use them on their own.

One way to use a parser is the `parseString` method. This will return
the structure of tokens, if it is a match, or throw a `ParseException`
if not.

``` text
    >>> print(test_values)
    ('1', now(), '" . $var1 "')
    >>> result = values.parseString(test_values)
    >>> print(result)
    [['1', 'now()', '$var', '3']]
    >>> print(result["values"]["danger identifier"])
    ['$var']
    >>> print(values.parseString("not a list of values")
    ...
    pyparsing.ParseException: Expected "(" (at char 0), (line:1, col:1)
```

The function `scanString` looks for substrings that match the grammar.
Quite useful. It also tells you where the substring was found. We use it
to tell the user the line and column where the potential `SQL` injection
was found:

**How to use `pyparsing.scanString`.**

``` python
for tokens, start, end in sql_injection.scanString(content):
    sqli_line = line(start, content)
    print("In file {0}, line {1}, col {2}:\n{3:^}"
          .format(path.split("/")[-1], lineno(start,content),
          col(start,content), sqli_line.strip() ))
```

These are just some of the `pyparsing` built-in helper functions
mentioned earlier: `scanString` returns an iterator which gives
`tokens`, just like `parseString()`, but also starting and ending
'characters'. To convert them to 'line' and 'column' numbers, we use the
functions `lineno()` and `colno()`, respectively.

Where parsers actually beat regular expressions is in extracting
information and structure from the input, as we did above to identify
the inserted values and from those, which are the variables where we can
inject `SQL`. For that, we need to parse again because we don’t know
beforehand whether the inserted value is a function call or a `PHP`
identifier:

``` python
injectable_variables = tokens["values"]
for injectable_variable in injectable_variables:
    res = (php_identifier ^ php_funcall).parseString(injectable_variable)
    injectable_variable = res["phpvar"]
    print(" Injectable variable {0}. Other occurrences:".format(injectable_variable))
```

Remember we need to detect lines with `SQL` queries that contain
dangerously concatenated variables, but also 'where' those variables are
taken from user input and whether they are protected. But since we
already have the `` `injectable variable''
as a regular `string ``, we can create 'yet another' parser on-the-fly
to find the lines where that variable is mentioned. This one is simple:

``` python
tpar = Literal(injectable_variable)
for tokens, start, end in tpar.scanString(content):
    print("  L{0:<3} {1}".format(lineno(start2, content),
                                 line(start2,content).strip()))
```

Finally, we run this code for every `PHP` file in the `bWAPP` server
root. The output we get is very long (see the [full
report](results.txt)) Here is part of it:

``` text
    In file sqli_4.php, line 131, col 17:
    $sql = "SELECT * FROM movies WHERE title = '" . sqli($title) . "'";
     Injectable variable $title. Other ocurrences:
      L129 $title = $_REQUEST["title"];
      L131 $sql = "SELECT * FROM movies WHERE title = '" . sqli($title) . "'";
    Found 1 SQL injection in bWAPP/sqli_4.php.
    ...
    In file sqli_1.php, line 143, col 13:
    $sql = "SELECT * FROM movies WHERE title LIKE '%" . sqli($title) . "%'";
     Injectable variable $title. Other ocurrences:
      L141 $title = $_GET["title"];
      L143 $sql = "SELECT * FROM movies WHERE title LIKE '%" . sqli($title) . "%'";
    Found 1 SQL injection in bWAPP/sqli_1.php.
    ...
    In file xss_stored_1.php, line 253, col 31:
    $sql = "SELECT * FROM blog WHERE owner = '" . $_SESSION["login"] . "'";
     No dangerous concatenations in this query.
    ...
    Total SQL injections found: 56
```

Boy, that’s a load of `SQL` injections\! However, some of these matches
might be a 'false positive' and maybe some files have 'escaped' our
scrutiny.

To find the ratio of discovered vulnerabilities to existing ones (the
'yield'), consider the 57 `SQLi` in
[Netsparker](http://www.mmebvba.com/sites/default/files/downloads/bWAPP_sample_report.pdf)
Compared to our 56, that gives us a 'yield' of 98%. Not too shabby for
our simple parser. Hence the 'escapes' is 2% in this case.

Given the parser design, and checking the script output, we see that
only really dangerous concatenations are reported. Thus we might say,
with a statistically sound 95% confidence, that our `pyparsing` parser
reports

> zero false positives.

## References

- McGuire, Paul (2008). 'Getting started with pyparsing'. O’Reilly
  shortcuts.

## Appendix: Full SQLi parser

Download [code](./sqli-parser.py) and [test cases](./test-cases.lst).
Run from the root of the tested `PHP` server.

**`sqli_parser.py`.**

``` python
"""
Module sqli-parser.py
Module to detect SQL insertions and selections that include
PHP variables or function calls in concatenations,
which is considered dangerous. Also finds other occurrences
of the dangerously concatenated variable in the same file.
"""

import contextlib
import os
from pyparsing import (
    alphanums,
    CaselessKeyword,
    col,
    Combine,
    delimitedList,
    Group,
    line,
    lineno,
    Literal,
    Optional,
    ParseException,
    Word,
    ZeroOrMore,
)

KW_INSERT = Combine(Literal('"') + CaselessKeyword("INSERT INTO"))
KW_VALUES = CaselessKeyword("VALUES")
KW_END = Literal('"')
KW_SELECT = CaselessKeyword("SELECT")
KW_FROM = CaselessKeyword("FROM")
KW_WHERE = CaselessKeyword("WHERE")
# $var_name_3
PHP_IDENTIFIER = Combine(Literal("$") + Word(alphanums + "_")).setResultsName(
    "phpvar"
)
# db2_table_1, column_1
SQL_IDENTIFIER = Word(alphanums + "_")
COLUMN_NAMES = Literal("(") + delimitedList(SQL_IDENTIFIER) + Literal(")")
VARCHAR = Literal("'").suppress() + Word(alphanums) + Literal("'").suppress()
# now(), mysqli_real_escape_string($link, $secret)
PHP_FUNCALL = Combine(
    Word(alphanums + "_")
    + Literal("(")
    + Optional(delimitedList(PHP_IDENTIFIER))
    + Literal(")")
)
# '" . validate($user_input) . "' or LIKE '%" . $var . "%'
DANGER_CONCAT = (
    Literal("'").suppress()
    + Optional("%")
    + Literal('"').suppress()
    + Literal(".").suppress()
    + (PHP_IDENTIFIER | PHP_FUNCALL)
    + Literal(".").suppress()
    + Literal('"').suppress()
    + Optional("%")
    + Literal("'").suppress()
).setResultsName("danger identifier")
VALUE = VARCHAR ^ PHP_FUNCALL ^ DANGER_CONCAT
VALUES = Group(
    Literal("(").suppress() + delimitedList(VALUE) + Literal(")").suppress()
).setResultsName("values")
WHAT_TO_SELECT = Literal("*") ^ delimitedList(SQL_IDENTIFIER)
# name='" . $name . "'
COND_COL_EQ_VAL = SQL_IDENTIFIER + Literal("=") + VALUE
# name LIKE '%".$name."%'
COND_COL_LIKE_VAL = SQL_IDENTIFIER + Literal("LIKE") + DANGER_CONCAT
ATOM_COND = COND_COL_EQ_VAL | COND_COL_LIKE_VAL
CONNECTOR = CaselessKeyword("OR") ^ CaselessKeyword("AND")
# col_user = '" . $user . "' AND password = '" . hash($password) . "'
CONDITION = Group(
    ATOM_COND + ZeroOrMore(CONNECTOR + ATOM_COND)
).setResultsName("values")
# "INSERT INTO blog VALUES (now(), 'a', '" . $inj1 . "','" . $inj2 . "')";
SQL_INSERT = (
    KW_INSERT
    + SQL_IDENTIFIER
    + Optional(COLUMN_NAMES)
    + KW_VALUES
    + VALUES
    + KW_END
)
# "SELECT * FROM ta_ble WHERE name = '" . $name . "'";
SQL_SELECT = (
    KW_SELECT
    + WHAT_TO_SELECT
    + KW_FROM
    + SQL_IDENTIFIER
    + Optional(KW_WHERE + CONDITION)
)
SQL_INJECTION = SQL_INSERT ^ SQL_SELECT


def scan_test_file(path="test-cases.lst"):
    """Scan an entire file to test for occurrences of SQL_INJECTION parser,
    determine what the injectable variables are and parse again looking for
    other occurrences of that variable."""
    with open(path) as test_file:
        content = test_file.read()
        print("\nScanning file {}".format(path))
        queries = 0
        for tokens, start, _end in SQL_INJECTION.scanString(content):
            sqli_line = line(start, content)
            print(
                "In file {0}, line {1}, col {2}:\n{3:^}".format(
                    path.split("/")[-1],
                    lineno(start, content),
                    col(start, content),
                    sqli_line.strip(),
                )
            )
            try:
                injectable_variables = tokens["values"]
                for injectable_variable in injectable_variables:
                    # If parse fails or key "phpvar" does not exist,
                    # there is simply no danger variable.
                    with contextlib.suppress(ParseException, KeyError):
                        # Re-parsing is ugly but necessary since a PHP_FUNCALL
                        # might not contain any PHP_IDENTIFIERs.
                        res = (PHP_IDENTIFIER ^ PHP_FUNCALL).parseString(
                            injectable_variable
                        )
                        injectable_variable = res["phpvar"]
                        print(
                            " Injectable variable {0}. Other ocurrences:".format(
                                injectable_variable
                            )
                        )
                        # Make a parser on-the-fly to detect other
                        # occurrences of the injectable variable
                        tpar = Literal(injectable_variable)
                        for _tokens2, start2, _end2 in tpar.scanString(
                            content
                        ):
                            print(
                                "  L{0:<3} {1}".format(
                                    lineno(start2, content),
                                    line(start2, content).strip(),
                                )
                            )
                        queries += +1
            except (ParseException, KeyError):  # Same as above
                print(" No dangerous concatenations in this query.")
        print("Found {0} SQL injections in {1}.".format(queries, path))
        return queries


def test_directory():
    """Iterate scan_test_file() for all source files in a directory
    and report total number of SQL injection vulnerabilities."""
    path = "./"
    vulns = 0
    for filename in sorted(os.listdir(path)):
        if filename.split(".")[-1] == "php":
            vulns += scan_test_file(path + filename)
    print("\nTotal SQL injections found: {}".format(vulns))


scan_test_file()
# test_directory()
```
