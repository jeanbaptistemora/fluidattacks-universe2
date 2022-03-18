---
slug: eight-vulnerable-package-managers/
title: Eight Is Bad News
date: 2022-03-18
subtitle: Buggy package managers, some only on Windows
category: attacks
tags: cybersecurity, application, social-engineering, vulnerability, windows, injection
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1647610000/blog/eight-vulnerable-package-managers/cover_managers.webp
alt: Photo by Timothy Dykes on Unsplash
description: Researchers found vulnerabilities in some versions of eight popular package managers. We review how an attacker could exploit them and urge everyone to upgrade.
keywords: Libraries, Package Managers, Open Source, Composer, Vulnerability, Windows, Software, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/OCijE83d7Sw
---

If you follow our blog,
you probably know
that we are all about keeping open-source libraries updated.
Development teams use these libraries to develop software,
so they don't need to start from scratch.
Depending on the language in which it is written,
most software uses dozens,
hundreds or even thousands of open-source libraries.
Our post about the newest [OWASP Top 10](../owasp-top-10-2021/)
reported how
using vulnerable and outdated components represents a bigger threat nowadays.
What follows is that teams need to establish processes
to manage their open-source libraries efficiently.

To no one's surprise,
developers have found a way to make their work easier
by using package managers.
We are talking about systems or tools
that help them automate processes
related to managing third-party open-source libraries.
These processes include installation,
upgrade and configuration.
What *is* surprising
is that recently,
and concurrently,
**eight** popular open-source package managers were reported
to have vulnerabilities.

The recent [discovery](https://blog.sonarsource.com/securing-developer-tools-package-managers)
was made by researchers
at code security solutions provider Sonar.
On March 8,
they listed the names,
versions,
CVE IDs
and whether there's already a patch.
The affected package managers are
[Composer](https://getcomposer.org/),
[Bundler](https://bundler.io/),
[Bower](https://bower.io/),
[Poetry](https://python-poetry.org/),
[Yarn](https://yarnpkg.com/),
[pnpm](https://pnpm.io/),
[pip](https://pip.pypa.io/en/stable/)
and [Pipenv](https://pipenv.pypa.io/en/latest/).

PHP, Ruby, Python, JavaScript, HTML, CSS, you name it!
Developers must examine libraries in these languages cautiously
when intending to use them with their package managers.

## Those vulnerable to command or argument injections

The vulnerability in Composer,
for libraries written in the PHP language,
is quite critical,
with a CVSS v3 score of [9.8](https://nvd.nist.gov/vuln/detail/CVE-2021-41116).
This package manager's vulnerable versions fail
to properly neutralize special elements used in a command.
So,
a threat actor can execute a command of their choosing
by injecting malicious new items into an existing command.
This is a [command injection attack](https://capec.mitre.org/data/definitions/248.html)
that results in modifying the interpretation
away from what the victim originally intended.

The flaw ([CVE-2021-41116](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41116))
is present
in the `browse` command
when running Composer on Windows machines.
This command can open a package's source and documentation.
Users need to type the name of the package as the argument,
and the command will open the URL of that package's homepage.
At least it seems.
Because this URL can be corrupted by a threat actor
to execute several other commands.
This includes downloading payloads in the background.
The attacker needs to phish the victim
into using the package for all this to happen,
though.
The researchers [recommend](https://blog.sonarsource.com/securing-developer-tools-package-managers)
running commands
with argument lists and using reliable escaping functions.
This would restrict customization,
reducing the risk of suffering an attack.

Moving on to a somewhat similar kind of attack:
Vulnerable versions of Bundler,
a package manager for application dependencies in Ruby,
and Poetry,
a manager for those written in Python,
don't properly neutralize the argument delimiters in a command.
Poetry fixed this issue in version 1.1.9,
but the researchers shared little information about it
and the CVE is pending.
So,
to understand what kind of attack could exploit vulnerabilities
in both managers,
we'll use the available information regarding Bundler's.

The severity of Bundler's vulnerability ([CVE-2021-43809](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-43809))
is high,
with a CVSS v3 score of [7.3](https://nvd.nist.gov/vuln/detail/CVE-2021-43809).
When victims invoke `git` commands,
that allows interpreting several user-controlled arguments
that could be maliciously crafted.
What attackers could do is create a Gemfile
(i.e.,
a file that describes the libraries —gems— used in a program)
declaring a dependency that is located in a Git repository.
But also [injecting arguments](https://capec.mitre.org/data/definitions/6.html)
that would fool Bundler into executing malware.
Again,
attackers need to [phish](../phishing/) the victim;
in this scenario,
into using the malicious Gemfile.
As it requires considerable user interaction,
exploitation is not as easy
as in the relatively straightforward command injection,
making it less critical.

## Most have an untrusted search path weakness

Imagine a person gives you the exact route to where they ask you to go.
Now imagine another scenario:
This person doesn't give you any clue other than the name of the destination,
say,
a Starbucks.
When the destination could be any of many,
there's confusion.
Let's get back to package managers:
If you don't specify the path to a file you want to run in the command,
the operating system will have to look for it only by its name.
Supposedly safe locations are stored in a variable called `PATH`.
Most operating systems will look for the file there,
but Windows will look first at the current working directory
and then `PATH`.

What is considered an [untrusted search path](https://cwe.mitre.org/data/definitions/426.html)
weakness is present in Yarn,
which manages libraries written in JavaScript.
The vulnerability in versions up to 1.22.13
allows fetching a file that is outside `PATH`.
If the working directory has an untrusted file
with the same name referenced in the command,
that means trouble.
The researchers mention the possibility
of a victim trying to fetch a library from a Git repository
by typing only "git" without its path,
and there being a malicious git.exe file in the working directory.
This would cause Yarn to fetch the malicious file.

The untrusted search path weakness was also discovered
in Bower ([CVE-2021-43796](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-43796);
affecting libraries in HTML,
CSS
and JavaScript),
pnpm (JavaScript),
pip (Python)
and Pipenv (Python).
But also in Composer and Poetry.

pip and Pipenv decided not to fix this issue.
[Reportedly](https://blog.sonarsource.com/securing-developer-tools-package-managers),
because "there are several other ways
[...]
an attacker could gain code execution in the same attack scenario."
Composer didn't have this scenario in their threat model,
so they chose not to address it.
But the rest did address it.
Yarn,
for example,
now uses a command called `where`
and allows the search
to be done only in locations defined in `PATH`.

## Be wary of your library choices

What's most interesting about the vulnerabilities we addressed in this post
is that developers have to be tricked into fetching malicious libraries.
Attackers have to rely on [social engineering](../social-engineering/)
or sneak malicious files into a trusted codebase.
This could sound like a relief,
but,
in earnest,
this whole situation highlights the importance of developers
being aware of the libraries they're using
and how they behave.
It also wouldn't hurt to learn [some indicators](../choosing-open-source/)
to have in mind when choosing open-source.
All the while,
let's remember what's key: Upgrade! Upgrade! Upgrade!

At `Fluid Attacks`,
we help you ensure
that the libraries you use in your software have no vulnerabilities.
[Contact us](../../contact-us/)\!
