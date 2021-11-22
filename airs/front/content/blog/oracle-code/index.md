---
slug: oracle-code/
title: The Oracle of Code
date: 2018-03-02
subtitle: About code as data
category: attacks
tags: testing, application, detect
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330963/blog/oracle-code/cover_fqvnfc.webp
alt: Code on a screen
description: This blog post is a description of the code-as-data approach
  to source code analysis.
keywords: Testing, Database, Code, Query Language, Semmle, Data,
  Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/hvSr_CVecVI
---

\`\`Most programs are too large to understand in complete detail''. This
was written in the 80’s.[<sup>\[1\]</sup>](#r1) Imagine the situation
today. Hence the need for automated tools to aid in the process of
analyzing code. The solution, according to [Oege de
Moor](https://lgtm.com/blog/code_as_data) from
[Semmle](https://semmle.com/), is obvious: treat code 'as data'.

This idea is not really new: Already in 1983, Mark Linton discussed that
programmers select 'views' to understand some 'aspects' of the code
base. This is already database-talk. It was only natural to propose
making a database out of the program structure, in order to be able to
ask questions about the program’s behavior.

Mere text analysis is not enough to understand the way variables are
used, the idioms and idiosyncrasies of the programming language, the
efficiency and complexity of your code, etc. In other words, we want to
understand the 'semantics' of your program, as well as its 'structure',
not just the syntax.

The most common way to represent interrelated, structured data is via
'relational databases'. These are typically queried via the `SQL`
language, which features simple, almost english-like queries, but is
very limited. As we’ll see, the database for a program’s source code
will be even more so. Thus the query system must be as advanced, but not
so much that it would hurt performance.

## Databases out of programs

Languages like `lisp` have an inherent 'code as data' mantra: every line
of code is a piece of manipulable data and vice versa. Markup languages
like `XML` have their own `` `database'' of sorts,
the `DOM ``, which can be queried via `XPath`.

But what about commonly used languages like `Java` and `Python`? To
every program we can associate a tree, called the 'abstract syntax tree'
(`AST`) which sort of displays the syntactic structure of the code.
Consider this `Ada` snippet from Linton’s thesis:[<sup>\[1\]</sup>](#r1)

**Sample `Ada` code.**

``` ada
prevmax := max;
if a > b then
    max := a;
else
    max := b;
end if;
```

Quite simple, but the same cannot be said about its `AST`. We have three
assignments (`:=`), one `if-then-else` conditional and five variables,
all interrelated, and all that has to be shown on the tree. The `AST`
would be like this:

<div class="imgblock">

!["Abstract syntax tree"](https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_800/v1620330962/blog/oracle-code/ast_g4ei72.webp)

<div class="title">

Figure 1. Adapted from [Linton’s original
diagram.](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1983/CSD-83-164.pdf#page=31)

</div>

</div>

Next, how do we make a database out of this? Neither `Semmle` nor other
players in the 'application intelligence' field such as
[CAST](http://www.castsoftware.com/) and [Modern
Systems](http://modernsystems.com/) tell us much about the process,
since obviously the magic behind their products must be there, but let’s
try to learn it ourselves from Linton’s ideas.

For the purposes of this article, it suffices to think of a database as
a set of entities joined by some relations. Now, the relevant entities
for source code analysis would be, as you expect, variables,
conditionals, functions, but also statements, expressions and
assignments. Further, some bits of code may actually be several kinds at
the same time. So you get an idea of the complexity of such a database.

For the code snippet above, Linton shows the [actual
tables](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1983/CSD-83-164.pdf#page=32)
and relations cut to the most relevant parts. I’ll try to simplify that
further by reducing it to an informal [entity-relationship
diagram](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model).
Here you can read unlabeled relations as \`have' or \`is' (generic
relations).

<div class="imgblock">

!["ER diagram for program database"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330960/blog/oracle-code/er_s9q9sb.webp)

<div class="title">

Figure 2. ER diagram for a simple code snippet

</div>

</div>

The most basic entity is the `statement`, which is basically every line
of code. It can be a `conditional`, an `assignment` or maybe a function
call (`fcalls`). An `assignment`, in turn, sets the value of the
left-hand-side variable to that of the right side. `Variables` are
related to the entity `type` (v.g. `int`, `String`, etc) and `name`.

This is only a subset of our already reduced model of the database. And,
hey, it’s only a model, which barely begins to compare to compare with
the actual database.

A typical 21<sup>st</sup> century `Java` program takes around 77 tables
(\!), according to Oege de Moor. This justifies our previous claim that
a powerful query language is needed to work with such a database. And
the guys at `Semmle` set out to do just that, and that is what
differentiates them from competitors.

## A query language to rule them all

The query language should be simple like `SQL`, but more powerful,
including Object-Oriented Programming (`OOP`) constructs and be able to
compose queries using logical connectors and quantifiers, like the
logical programming language [`Prolog`](http://www.learnprolognow.org/).
However, this would add too much overhead, so a smaller subset called
[`Datalog`](http://www.learndatalogtoday.org/) was chosen as the basis
for the tailor-made `QL` language.

This query language can be used to locate code defects. For example, in
`OOP`, when defining the notion of equality in a class, one usually
needs to define a hash function, because object equality should imply
hash equality. So, let’s look for classes that declare an `equals()`
method but not a `hashCode()` method using `QL`:

**`QL` example from [\[2\]](#r2).**

``` sql
from Class c
where c.declaresMethod("equals") and
    not( c.declaresMethod("hashCode") ) and
    c.fromSource()
select c.getPackage(), c
```

The clauses are similar to `SQL`, but there are object-like constructs
(`Class c`) which have their own methods (`c.declaresMethod()`) and the
logical connectors work a bit differently from `SQL` and have a larger
scope. In `QL`, one can:

- define and use 'predicates' in queries (expressions that can be true
  or false depending on the parameters),

- use logical quantifiers (for all, exists) in order to simplify
  aggregation and grouping (find the number of lines of code in a
  given package), which is complicated in `SQL`

- define generic queries that can be inherited and overridden, just
  like in `OOP`

We cannot go further into the details of `QL` here, but instead let’s
focus on what we can do with it.

## Applications

When you can ask questions about your code to an omniscient oracle, you
can really bring the \`\`data age'' into your development flow.

You can use the 'code-as-data' approach to:

- increase productivity by computing metrics about the development
  process,

- ensure the following of coding standards and whichever development
  model your team has chosen,

- objectively determine the quality of the code, and

- find security bugs and vulnerabilities.

This is what interests us most. `Semmle` maintains a public queries
[repository](https://github.com/lgtmhq/lgtm-queries) and a
[website](https://help.semmle.com/wiki/) with general rules that should
be followed for some of the supported languages, namely, `Java`, `C`,
`Python` and some of their derivatives. Included are some security
guidelines, with their corresponding `CWE`. For example, we can detect
`XSS` in `Java` with this query:

**`Java XSS` detection query.**

``` sql
import semmle.code.java.security.XSS
from XssSink sink, RemoteUserInput source
where source.flowsTo(sink)
select sink, "Cross-site scripting vulnerability due to $@.",
source, "user-provided value"
```

And it would detect this kind of vulnerable code, which does not
properly validate user input:

**`XSS`-vulnerable `Java` code. Via
[Semmle](https://help.semmle.com/wiki/pages/viewpage.action?pageId=1607941).**

``` java
public class XSS extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
        // BAD: a request parameter is written directly to an error response page
        response.sendError(HttpServletResponse.SC_NOT_FOUND,
                "The page \"" ` request.getParameter("page") ` "\" was not found.");
    }
}
```

No query for the vulnerability you’re testing for? That’s what the `QL`
language is for. You just write your own query.

To wrap this up with more spectacular examples, here is a query to find
[`Heartbleed`](http://heartbleed.com/)-like vulnerabilities:

**`QL` to detect `Heartbleed`.**

``` sql
from FunctionCall memcpy, Struct s, Field f, Field g, float perc
where f = s.getAField() and g = s.getAField() and
      memcpy(memcpy, f) and
      memcpy_usually_guarded(f, g, perc) and
      not guarded_memcpy(memcpy, f, g) and
      forall (Field gg, float pperc | memcpy_usually_guarded(f, gg, pperc) | pperc <= perc)
select memcpy, "memcpy from " ` s.toString() ` "::" ` f `
               " is guarded by comparison against " ` s.toString() ` "::" ` g `
               " in " ` perc ` "% of all cases, but not here."
```

Notice the universal quantifier (`forall`) we mentioned earlier, and
also that this is not the full query, since it is based upon predicates
that have to be defined 'ad hoc' in addition to built-in ones. See the
full query and a discussion at
[Semmle](https://semmle.com/developing-a-custom-analysis-to-find-heartbleed-like-security-vulnerabilities/).

The `Apache Struts` vulnerability
[`CVE-2017-9805`](https://nvd.nist.gov/vuln/detail/CVE-2017-9805) — related
but not to be confused with
[`CVE-2017-5638`](https://nvd.nist.gov/vuln/detail/CVE-2017-5638) — the
one that was exploited in the `Equifax`
[breach](https://www.equifaxsecurity2017.com/), was
[found](https://lgtm.com/blog/apache_struts_CVE-2017-9805_announcement)
and announced by [`lgtm.com`](https://lgtm.com/). Through this service
`FOSS` projects can take advantage of ``Semmle’s technologies in
application intelligence,
as long as their repository is open on `GitHub``.

The basic idea is simple enough: look for deserialization of untrusted
(i.e., user-controlled) data. In this particular case, we’re interested
in the flow of data from a `ContentTypeHandler` which gets the input to
an unsafe deserialization method. The query text reflects just this
idea:

**See [Finding Unsafe Deserialization with
QL.](https://lgtm.com/blog/finding_unsafe_deserialization_with_ql).**

``` sql
from ContentTypeHandlerInput source, UnsafeDeserializationSink sink
where source.flowsTo(sink)
select source, sink
```

Again, this is not the full query. See the [`lgtm`
blog](https://lgtm.com/blog/apache_struts_CVE-2017-9805) entry on this
discovery.

`Semmle` has thus made into a reality what was deemed impossible time
and again for 30 years: bring data analysis techniques and source code
analysis together. This powerful combination has already paid off for
users like `NASA` and `Google`, as well as countless `FOSS` projects.
Only the
[Pythia](http://dante.udallas.edu/hutchison/Mythology/Other/pythia.htm)
knows what the future of the code-as-data approach will bring.

## References

1. [Mark Linton (1983). 'Queries and views of programs using a
    relational database system'. PhD thesis, UC
    Berkeley.](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1983/CSD-83-164.pdf)

2. [Oege de Moor et al. (2007). 'QL for source code analysis'. Keynote
    address. Source Code Analysis and
    Manipulation.](https://ieeexplore.ieee.org/document/4362893)
