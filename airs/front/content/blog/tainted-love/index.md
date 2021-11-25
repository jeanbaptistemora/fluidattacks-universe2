---
slug: tainted-love/
title: Tainted Love
date: 2019-08-30
subtitle: It's all about sanitization
category: attacks
tags: vulnerability, code, discovery
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331105/blog/tainted-love/cover_pkrmla.webp
alt: Person using a Syringe filled with bad stuff
description: This blog post provides a brief description of static and dynamic
  taint analysis or taint checking.
keywords: Taint Analysis, Security, Injection, Bug, Vulnerability, Flow,
  Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/55HNtDVObk8
---

In several past articles, we have briefly touched on the concept of
taint analysis. In this article, we will fill in the knowledge gaps
regarding taint analysis which may have resulted from our previous
references. On one hand, this concept is intimately linked with code
representations used by some of the `ML`-powered vulnerability detectors
we have presented before, and on the other hand, it is well-complemented
by symbolic execution, so we deemed it necessary to clarify this concept
a bit.

Most of the `OWASP` top 10 web application vulnerabilites arise because
an attacker can inject some code into the application’s inputs which are
then used to perform some action in the server. The classic example for
this is the `SQL` injection.

For example, this page from `bWAPP` has an input where the user is
supposed to write a movie name, which should contain only alphanumeric
characters:

<div class="imgblock">

![bWAPP movie search](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330880/blog/fuzzy-bugs-online/scr-bwapp-movie-search_qh3gye.webp)

<div class="title">

Figure 1. bWAPP movie search

</div>

</div>

Some movies will occasionally have punctuation marks such as a dash or a
question mark. Here is what this page does with the user input:

**Adapted from [bWAPP
code](https://github.com/theand-fork/bwapp-code/blob/master/bWAPP/sqli_6.php).**

``` php
$title = $_POST["title"];
$sql = "SELECT * FROM movies WHERE title LIKE '%" . $title . "%'";
$recordset = mysql_query($sql, $link);
```

The input is taken from the `POST` request and pasted right into a `SQL`
query which is immediately performed and shown to the user in a table.
If instead of an actual movie name, an attacker writes this in the box:

``` sql
%' UNION SELECT id, login, password, email, secret,
activated, admin FROM users;#
```

Then the `SQL` query becomes this:

``` sql
SELECT * FROM movies WHERE title LIKE '%%'
  UNION SELECT id, login, password, email, secret,
  activated, admin FROM users;
```

And all the movies' information is retrieved, along with the users'
login information:

<div class="imgblock">

![bWAPP SQLi](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330880/blog/fuzzy-bugs-online/scr-succesful-sqli_vlv6cg.webp)

<div class="title">

Figure 2. Tainted!

</div>

</div>

The user input has become *tainted*, and hence the `SQL` query is now
taintedas well. In the context of taint checking the `$title` input
above is called a *source*, which is where the bad input and the
possible injection is coming from.

What is the problem with tainted inputs? it depends on what is done with
them, i.e., at the *sink*, where the input is consumed. As we have
stated in past articles illustrating other injection- or *taint-style*,
this can be avoided with input validation and sanitization. So
basically, simply check that the input is valid and fix it if it’s not
by removing dangerous characters or only allowing known good ones.

*Taint analysis* or *taint checking* consists of identifying all sources
of potentially dangerous user input, all security-critical sinks such as
system calls, process interactions, invoking shells, altering files,
etc, and figure out if there is any sanitizers between each source-sink
pair:

<div class="imgblock">

![Taint analysis depiction](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330670/blog/big-code/taint-analysis_fz03sg.webp)

<div class="title">

Figure 3. Taint analysis diagram via [Coseinc](http://web.cs.iastate.edu/~weile/cs513x/5.TaintAnalysis1.pdf).

</div>

</div>

Then, depending on whether this taint analysis is *static* (code) or
\_dynamic (runtime), the taint-checking tool should either report to the
developer so they can fix the issues or avoid the execution of
security-critical operations at the sink level based on data that has
been tainted, respectively.

## Dynamic taint analysis: the Perl approach

The `Perl` programming language is well-known for having used taint
analysis as early as 1989. It is one of its main built-in security
features, as can be seen by browsing
[perlsec](https://perldoc.perl.org/perlsec.html).

The `Perl` approach to taint checking is simple:

- Treat every input as tainted.

<!-- end list -->

``` perl
my $name = $cgi->param("name");  # Get the $name from user input, tainted!
```

- Any line of code that contains a tainted variable implies that any
  assigned variables in that line are also tainted.

<!-- end list -->

``` perl
my $full = $name."@fluidattacks.com";  # Now $full is also tainted
```

- A tainted variable can only be untainted by \_laundering it via
  regular expressions:

<!-- end list -->

``` perl
if ($full =~ /^([-\@\w.]+)$/) {
    $full = $1;                    # $full now untainted
}
```

- No tainted variable can be used in any risky command, such as
  invoking a sub-shell, opening files, interacting with system
  processes, etc. That’s the real run-time protection. Thus the
  following SQL `query` would fail:

<!-- end list -->

``` perl
$dbh->execute("SELECT * FROM users WHERE email = '$full';");
```

All a user needs to do to enable taint mode in `Perl` is add the `-T`
switch when running from the command line or in the case of executable
scripts, such as `CGI` scripts (a common use case for `Perl`), add that
switch to the `shebang`:

``` perl
#!/usr/bin/perl -T
```

It is worth noting that, since `Perl` is an interpreted scripting
language, this taint mode is only a run-time protection which might not
be bulletproof and also might block legitimate requests.

## Static analysis: the PyT approach

`PyT` is a static taint-checking tool for detecting security
vulnerabilities in `Python` web applications. More specifically, it was
designed with `Flask` applications in mind. It was developed as a
Master’s thesis project by Stefan Micheelsen and Bruno Thalman at
Aalborg University.

We chose this as an example of static taint checking not for its
results, but rather for the very well-written and easy to understand
thesis that explains PyT inner workings and hence, the theory behind
static taint analysis. Regarding the actual results component, I got 0
vulnerabilities in our own projects when using this tool and, curiously
in the tiny but bug-ridden [Damn Small Vulnerable
Web](https://github.com/stamparm/DSVW) application as well.

As you might now expect, taint analysis is linked to the flow of
information inside the program, which can be more accurately represented
by the program’s *Control Flow Graph*. They use as basis for a
mathematical model known as a *lattice*, which has an interesting
property, all monotone (steadily increasing or decreasing) functions
defined on them have a fixed point, they eventually stand still. As it
happens, code reachability and data flow can be represented in terms of
equations on this lattice. These are *guaranteed* to have a solution by
the fixed point property above. Here is a more friendly depiction of the
process, in the author’s own drawings:

<div class="imgblock">

![PyT process](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331103/blog/tainted-love/pyt-flow_tyb4na.webp)

<div class="title">

Figure 4. Overview of PyT’s process from [\[1\]](#r1)

</div>

</div>

The final step, of course, is reporting, so that the developer might
take the appropriate measures to fix the taint vulnerabilities.

---
The idea in both incarnations of taint analysis is simple but powerful.
Figure out the attack surface and make sure the tainted input can never
reach what you are trying to protect. Following this simple idea will
surely lead to more secure code. But if you are not sure, you can always
give a taint-checking tool a try.

## References

1. Stefan Micheelsen, Bruno Thalman. *PyT: A Static Analysis Tool for
    Detecting Security Vulnerabilities in Python Web Applications.* [MSc
    thesis](https://projekter.aau.dk/projekter/files/239563289/final.pdf)
