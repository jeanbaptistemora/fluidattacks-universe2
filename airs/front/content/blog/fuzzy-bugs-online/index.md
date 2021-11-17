---
slug: fuzzy-bugs-online/
title: Fuzzy Bugs Online
date: 2018-02-09
category: attacks
subtitle: Fuzz techniques for attacking web applications
tags: sql, fuzzing, injection
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330883/blog/fuzzy-bugs-online/cover_rsdc0v.webp
alt: Fuzzy caterpillar
description: How to make basic fuzz attacks on web apps? We fuzz over SQL
  injections on a vulnerable DB search site from bWAPP, using OWASP ZAProxy,
  obtaining mixed results.
keywords: SQLi, Fuzzing, Attack, Vulnerability, Security, Application,
  Pentesting, Ethical Hacking
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/Tv5AK37PVlA
---

In general, fuzzing means to try many inputs, well-formed or otherwise,
in an application, protocol or other interaction with a computer, that
it might trigger an unexpected behavior. Web fuzzing in particular is an
automated, computerized technique to find bugs and vulnerabilities
within a computer system. If you think protecting your site is a matter
of simply blocking the most common types of malicious requests, think
again. Read on for more.

## Injecting SQL into a vulnerable site

A fairly common situation is a website providing the ability to search,
add, and remove information from a database. But introducing this kind
of feature demands great care in how you set up and access that
database.

Let’s look at `bWAPP`, which has a movie database, and allows us to
search for a given title:

<div class="imgblock">

![bWAPP screenshot - movie search](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330880/blog/fuzzy-bugs-online/scr-bwapp-movie-search_qh3gye.webp)

<div class="title">

Figure 1. `bWAPP’s movie search site

</div>

</div>

It looks like the site takes the user’s input as a `POST` request, then
searches the database for that request, and finally prints back the
result in table form. We can tell it’s a `POST` request since there is
nothing in the `URL` that hints `GET` (consider that the huge `POST`
title wouldn’t be there in a real app).

Let’s check that using the `OWASP ZAP` proxy. Indeed, we can see and
confirm that the request is `POST`:

**`POST` request when you search for a movie.**

``` text
POST /sqli\_6.php HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (X11;
Linux x86\_64; rv:52.9) Gecko/20100101
Goanna/3.4 Firefox/52.9 PaleMoon/27.7.2
...
Content-Length: 24
title=the\&action=search
```

Now we can intercept this request using `ZAP` and edit the `title=the`
bit above, changing `the` by some `SQL`. For example, if we change it
to:

**Naive SQL injection.**

``` sql
Iron Man' OR 1=1;
```

Because the `1=1` is always true, making the overall condition true, we
should get all entries in the table.

But it doesn’t happen. We get an error:

``` text
Error: You have an error in your SQL syntax; check the manual
that corresponds to your MySQL server version for the right
syntax to use near '%'' at line 1
```

Well, at least now we know for sure they are using `MySQL`, because we
can see it in the error message.

There are infinitely many strings (sequences of characters) we could try
to use in order to complete the unknown `SQL` query the server is asking
from the database.

What if we could try a bunch of them, at the same time, automatically?

Well, that’s what \`\`fuzzing'' is all about.

## Web application fuzzing

There are other kinds of fuzzing: desktop application fuzzing using
command-line or graphical interfaces (testing combinations of buttons,
inputs, etc.), protocol fuzzing, file format fuzzing, and
more.[<sup>\[1\]</sup>](#r1%20)

In this article we will focus only on web application fuzzing which is
the semi-automated, pseudo-random manipulation of `URLs`, forms,
user-generated content[<sup>\[1\]</sup>](#r1%20), requests, etc. We may
tackle other kinds of fuzzing in future articles.

For a given fuzzing attack, the most comprehensive and sure-fire way to
succeed would be to try every possible input. For example, if we’re
fuzzing an input string, we should try every possible string, beginning
with the empty string. This is due to the fact that sometimes programs
have unexpected reactions to odd input, like the bug found in `Mac OS`
last year, where you could log in as root by pressing the login button
enough times (see
[CVE-2017-13872](https://nvd.nist.gov/vuln/detail/CVE-2017-13872#vulnDescriptionTitle)
for more info).

But this `` `try everything'' approach is not really feasible or
practical:
the space complexity of such an attempt
would be enormous.
Thus we must bound the so-called
'explorable solutions space'.
This is usually achieved by limiting
the input attempts to values
that have a statistically higher probability
of triggering a bug.
These are known as 'fuzz vectors'.
In our case,
they would be `SQL `` queries. Some examples from
`OWASP`:[<sup>\[2\]</sup>](#r2%20)

``` sql
' OR 1=1;--
' OR 'a'='a
%22`OR`isnull%281%2F0%29+%2F*
Admin' OR '
'%20SELECT%20*%20FROM%20INFORMATION_SCHEMA.TABLES--
HAVING 1=1--
' OR username LIKE char(37);
' ; DROP TABLE temp --
GRANT CONNECT TO name; GRANT RESOURCE TO name;
```

Your fuzzer of choice will probably provide a healthy dose of fuzz
vectors, as does ours, the `OWASP ZAP Fuzzer`. All we need to do is

1. select the string we want to fuzz,

2. invoke the fuzzer,

3. select the 'payloads', i.e. the fuzz vectors, and

4. run the fuzzer.

`ZAP` includes several of those by default; we will use the `SQL`
injection vector from `jbrofuzz`:

<div class="imgblock">

!["Running ZAP fuzzer"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330881/blog/fuzzy-bugs-online/anim-run-zap-fuzzer_b5xrj7.gif)

<div class="title">

Figure 2. How to run `ZAP` fuzzer

</div>

</div>

Successfully injected `SQL` queries are marked with the state
\`\`reflected'' in the list:

<div class="imgblock">

!["bWAPP fuzz testing - reflected SQL injections"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330879/blog/fuzzy-bugs-online/scr-reflected-fuzzed-injections_zcnizh.webp)

<div class="title">

Figure 3. Reflected `SQL` injections in fuzz attacks

</div>

</div>

Here we see a fuzz attack is only as good as its payloads or fuzz
vectors. Only the most trivial injections succeeded, i.e. the ones of
the form

``` sql
whatever' OR (something truthy)
```

which simply show all entries in the table `movies`.

When fuzzing, this is both a blessing and a curse. Usually, they don’t,
but occasionally the simplest injections reveal unexpected outcomes, and
when they do, they are real surprises such as the `Apple` bug mentioned
above.

## Comparison with manual injection

With information about the app and the database structure, we can inject
more effective queries. For example, suppose you’ve found out that there
is another table called `users` and we want to see what’s in there.

If we try to inject the following query:

``` sql
%'; SELECT * FROM users;
```

we get an error, because the database management system does not allow
query concatenation.

If we try with `union` instead:

``` sql
%' UNION SELECT * FROM users;#
```

we still get an error, because the tables don’t match in size.

Suppose, for the sake of the example, that we also know (or guess) the
names of the columns and select the most interesting ones:

``` sql
%' UNION SELECT id, login, password, email, secret,
activated, admin FROM users;#
```

Then we get the most of the users' info (passwords are hashed, but can
be [recovered](../storing-password-safely/)).

<div class="imgblock">

!["bWAPP SQL injection screenshot showing passwords"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330880/blog/fuzzy-bugs-online/scr-succesful-sqli_vlv6cg.webp)

<div class="title">

Figure 4. Succesful manual `SQL` injection

</div>

</div>

---
By itself fuzz testing cannot replace human expertise in the equation
but it adds an important additional point of view. As seen in the `Mac
OS` example, its greatest weakness can be a potential source of great
surprises. We have merely glimpsed the tip of the iceberg here, but hope
you find this short introduction helpful.

## References

1. [OWASP wiki article on
    Fuzzing](https://www.owasp.org/index.php/Fuzzing)

2. [OWASP Testing Guide appendix - Fuzz
    vectors](https://www.owasp.org/index.php/OWASP_Testing_Guide_Appendix_C:_Fuzz_Vectors)
