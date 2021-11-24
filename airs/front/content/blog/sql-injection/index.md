---
slug: sql-injection/
title: Such as Microbes Getting Into You?
date: 2021-08-09
subtitle: Don't leave the relentless SQL Injection in oblivion
category: attacks
tags: sql, injection, hacking, web, application, cybersecurity
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1628541914/blog/sql-injection/cover_sql_rpw56v.webp
alt: Photo by National Cancer Institute on Unsplash
description: Thanks to this post, you'll understand the injection attacks
  in general terms, especially the SQL Injection. You'll also have some
  prevention ideas at hand.
keywords: SQL, Injection, SQLi, Application, RDBMS, Input, Attack,
  Pentesting, Ethical Hacking
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/zoFbfT0M_BU
---

> Microbes have developed various ways of fooling the immune system —by
> sending out confusing chemical signals, for instance, or by disguising
> themselves as benign or friendly bacteria. Some infectious agents
> \[…​\] can trick the immune system into attacking the wrong
> organisms. —Bryson, [*The
> Body*](https://books.google.com.co/books?id=856DDwAAQBAJ)

Every person who frequently devotes their attention to the field of
cybersecurity most certainly recognizes the **OWASP Top 10 Project**.
However, without leaving aside any reader engaged here, we can say that
what this standard ["represents](https://owasp.org/www-project-top-ten/)
\[is\] a broad consensus about the most critical security risks to web
applications." This top 10 is an invaluable guide for software
developers in building secure code for organizations. Through this
standard, developers can see the error of their ways and make the
necessary changes before a catastrophe.

Leading the [OWASP Top
Ten 2017](https://owasp.org/www-project-top-ten/2017/), [in terms of
variables](https://owasp.org/www-pdf-archive/OWASP_Top_10-2017_%28en%29.pdf.pdf)
such as prevalence, detectability, exploitability, and impact, we find
the web application security risk
[Injection](https://owasp.org/www-project-top-ten/2017/A1_2017-Injection).
Within this risk, we have SQL Injection, our focal point in this new
blog post.

## Wait, first, what’s Injection?

In the Common Attack Pattern Enumeration and Classification
([CAPEC](https://capec.mitre.org/index.html)), "a community resource for
identifying and understanding attacks," we find a list of attack
patterns grouped into nine mechanisms. One of them is the category
called [Inject Unexpected
Items](https://capec.mitre.org/data/definitions/152.html). There, the
attack patterns "focus on the ability to control or disrupt the behavior
of a target either through crafted data submitted via an interface for
data input, or the installation and execution of malicious code on the
target system." **That’s Injection**. The attacker can *inject* input
(including instructions) that, in the interpretation of the application,
can provoke it to perform actions far from the original purpose and
reach instability. Something similar to what, in a biological setting,
some microorganisms can do to our immune system (see [Bryson’s
book](https://www.amazon.com/Body-Guide-Occupants-Bill-Bryson/dp/0385539304)).

Additionally, within that mentioned category in CAPEC, we have the "meta
level attack pattern" [Command
Injection](https://capec.mitre.org/data/definitions/248.html). There,
the attacker modifies an existing command string and, consequently, the
interpretation of a downstream component of the application, looking for
particular responses. The Command Injection is facilitated by weaknesses
in command building or input validation and can culminate in
exploitation. This pattern is the "parent of"
[LDAP](https://capec.mitre.org/data/definitions/136.html),
[XML](https://capec.mitre.org/data/definitions/250.html) and other
injections, including the one that concerns us now: [SQL
Injection](https://capec.mitre.org/data/definitions/66.html).

## Ok, what’s SQL Injection?

I think we should first pose the following question: What does SQL mean?
SQL refers to Structured Query Language, ["the standard
language](http://www.sqlcourse.com/intro.html) for relational database
management systems" (RDBMSs). It is used to establish communication with
relational databases, which can serve companies of all sizes to store
and analyze information and as the back end for online applications. So,
through SQL statements, also called
[*queries*](https://www.educative.io/blog/what-is-database-query-sql-nosql),
in an RDBMS, we can retrieve, add, delete and update data of a database.
Nowadays, [among the most commonly
used](https://www.statista.com/statistics/1131568/worldwide-popularity-ranking-relational-database-management-systems/)
RDBMSs worldwide, we can find Oracle, MySQL, Microsoft SQL Server, and
PostgreSQL.

Now, [as referenced in
CAPEC](https://capec.mitre.org/data/definitions/66.html), the SQL
Injection attack "exploits target software that constructs SQL
statements based on user input." This kind of input can be, for example,
your username and password to log in to a web application. The attacker
creates input strings that within the application give rise to SQL
statements oriented to different actions from those already predefined.
Basically, the attacker puts a metacharacter ["into data
input](https://owasp.org/www-community/attacks/SQL_Injection) to then
place SQL commands in the control plane, which did not exist there
before." That’s why the consequent procedure gives unexpected results.

To enlighten you a bit more, you can watch the example [in this
video](https://youtu.be/FHCTfA9cCXs?t=84). If you are interested in
something more technical, [here is a post](../sqli-manual-bypass/) from
one of our ethical hackers.

<div class="imgblock">

![Spiske](https://res.cloudinary.com/fluid-attacks/image/upload/v1628549604/blog/sql-injection/spiske_v0nev5.webp)

<div class="title">

Figure 1. Photo by [Markus
Spiske](https://unsplash.com/@markusspiske?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on [Unsplash](https://unsplash.com/photos/DnBtFBnqlRc).

</div>

</div>

As I said before, this type of attack can occur due to failures in the
software for input validation. In accordance with the corresponding
weakness listed as
[CWE-89](https://cwe.mitre.org/data/definitions/89.html) in the [Common
Weakness Enumeration](../../compliance/cwe/), the application "does not
neutralize or incorrectly neutralizes special elements that could modify
the intended SQL command." When the attacker introduces SQL syntax, and
the system does not validate it, they can obtain multiple advantages
thanks to the resulting queries.

Specifically, thanks to a successful SQL Injection, the attacker can
access a system without previous knowledge of credentials and can
*interact* with the database, for instance, to read sensitive
information and modify it as they wish. The attacker can also execute
administration processes (e.g., denial of services) and sometimes even
send commands to the operating system to compromise it.

I can’t deny the surprise I felt when I saw [what OWASP
said](https://owasp.org/www-community/attacks/SQL_Injection#) in
addition to the above: "The severity of SQL Injection attacks is limited
by the attacker’s skill and imagination, and to a lesser extent, defense
in depth countermeasures \[…​\]." What does this lead us to think?
Perhaps something like this: If we are reckless enough to leave software
vulnerable to SQL Injection, we better pray that it does not fall into
the clutches of a clever malicious hacker.

## So, what can we do?

This vulnerability, which is easy to detect and exploit, can be avoided
through several techniques that we can see widely exposed in the [OWASP
SQL Injection Prevention Cheat
Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).
However, in order to give you an overview, we can condense much of the
information presented there. As a first option, we have the use of
parameterized queries instead of dynamic queries. This alternative
forces developers to define the entire SQL code beforehand so that only
the required parameters are accepted for query execution afterward.
Thus, the database succeeds in distinguishing between code and data for
all types of inputs it receives.

As a close alternative to the previous approach, perhaps with the same
effectiveness, we have the use of stored procedures. Here, developers
define them and store them in the database itself to be called from the
application later. They are not something that users are able to give as
input. A third strategy strongly linked to the previous ones that can
act as a complement refers to [input
validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html).
In this case, criteria are created to detect unallowed data patterns and
prevent them from entering the application workflow.

Another option is offered by OWASP as a last resort, apparently due to
its weakness, when it’s impossible to use the above. "This technique is
to escape user input before putting it in a query." Here, the RDBMS
allows some particular character escaping schemes in specific queries so
as not to confuse the user input with the developer’s SQL code. Of
course, we cannot leave out an additional recommendation. It is to keep
the privileges of the database accounts to the *minimum* limit. Users
should have sufficient access permissions to perform their predetermined
tasks. Thus, for example, who only needs to read all or just a portion
of the database, does not need permissions to add or delete information.

Finally, at `Fluid Attacks`, we recognize how the security of your web
applications, and consequently that of your company’s and users' data,
can be affected by the widely used and dangerous SQL Injection attack
vectors. That’s why we help you identify with speed, accuracy, and at
the earliest stage if your software is vulnerable to SQL Injection.
Don’t hesitate to [contact us\!](../../contact-us/)
