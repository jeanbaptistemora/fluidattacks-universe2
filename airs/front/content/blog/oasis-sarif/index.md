---
slug: oasis-sarif/
title: Have You Read About OASIS SARIF?
date: 2022-08-03
subtitle: New companies come on board to renew this standard
category: politics
tags: code, software, company, cybersecurity, security-testing
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1659547166/blog/oasis-sarif/cover_oasis_sarif.webp
alt: Photo by Zdeněk Macháček on Unsplash
description: In this blog post, we provide an overview of the OASIS SARIF. More and more companies are joining OASIS to support the creation and launch of a new version.
keywords: Oasis, Sarif, Standard, Format, Static Analysis, Sast, Tools, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/83gB_koMuvA
---

These days,
[several companies](https://www.oasis-open.org/2022/05/31/influx-of-cybersecurity-leaders-sign-on-to-support-new-version-of-oasis-sarif-standard-for-detecting-software-vulnerabilities/)
worldwide are joining forces
to support the new version
of the OASIS Static Analysis Results Interchange Format (SARIF).
[SARIF](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=sarif),
in a nutshell,
is a standardized format for the output of static analysis tools.
In this post,
we will give you a quick overview of it.

Before taking a closer look at SARIF,
what is OASIS?
OASIS Open is [a non-profit organization](https://www.oasis-open.org/org/)
in which individuals and entities around the world come together
to collaborate in the transparent development of open code and standards
for technologies such as cybersecurity,
IoT and cloud computing.
[Five years ago](https://lists.oasis-open.org/archives/sarif/201708/msg00000.html),
OASIS Open issued a call for participation in a new technical committee (TC)
to its members and interested parties:
the SARIF TC.
The primary purpose of this group was to "define a standard output format
for static analysis tools."

As you know,
many tools use the static analysis technique
to assess the quality and security of software.
(At `Fluid Attacks`,
for example,
we use our SAST tool for vulnerability detection.
SAST stands for [Static Application Security Testing](../../product/sast/).)
It's called "static"
because the software under evaluation is not running
at that time.
When developers utilize several of these tools
to get different perspectives on the analyzed code,
they end up aggregating the results delivered
to have an overall picture of the software quality.
Tools producing results in various formats complicate this task.
Hence the value of defining a standard output format.

<cta-banner
  buttontxt="Read more"
  link="/solutions/security-testing/"
  title="Get started with Fluid Attacks' Security Testing solution right now"
/>

["Clearly](https://www.oasis-open.org/news/pr/industry-leaders-collaborate-to-define-sarif-interoperability-standard-for-detecting-softwar/),
people involved in static analysis appreciate the need for interoperability,
and they are committed to making it happen with SARIF,"
said Laurent Liscia,
CEO of OASIS Open,
back in 2017.
[The first version](https://github.com/oasis-tcs/sarif-spec/blob/master/Documents/working_draft_wikipedia_page.md)
of the OASIS SARIF standard
was released in March 2020
[after receiving by ballot](https://www.oasis-open.org/news/announcements/static-analysis-results-interchange-format-sarif-v2-1-0-is-approved-as-an-oasis-s/)
the affirmative consent of all members involved.
The standard was [named SARIF v2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
to recognize Microsoft's previous efforts and pre-standard versions.
Following this release,
discussions resumed again in March 2021 at the TC
on a possible new version of the standard.

As [Larry Golding](https://github.com/lgolding),
co-editor of the SARIF specification,
comments [in the introduction](https://github.com/microsoft/sarif-tutorials/blob/main/docs/1-Introduction.md)
of the [tutorial to the standard](https://github.com/microsoft/sarif-tutorials),
the multiple output formats
of the thousands of static analytic tools
bring with them problems such as the following:

- It's necessary to learn how to read all of them.

- There's no standard method to view and interact with all the tool outputs
  in the development environment (e.g., Visual Studio Code).

- There's no standard method to convert the outputs into bugs
  in issue-tracking systems (e.g., GitLab, GitHub).

- There's no standard method to create metrics
  (e.g., number of bugs in a software component).

SARIF,
a JSON-based format,
emerges as a solution to all these headaches.
So,
let's say you have several static analysis tools to assess your code
and identify programming and style errors,
non-compliance with legal requirements,
and security vulnerabilities,
among other things.
Suppose these tools,
although each has its own output format,
offer you the possibility of converting results into other formats.
Either with a formatter plugin
or with an external utility for report format conversion,
you could bring the results obtained in all your tools
into the unified SARIF format.
From there,
already knowing this type of file,
you could make a straightforward integration
and examination of your information.

For example,
you can achieve something like this
with the Microsoft SARIF Viewer extension for Visual Studio.
It can automatically convert more than 10 log file formats to SARIF
and integrates with the Visual Studio environment
to show you a user-friendly list of results with their respective details.
Among the details you might see,
apart from the name of the tool and the scanned files,
are the following:

- Information about the violated rule

- The severity of the violation

- The location of the flaw and code paths leading to it

- Suggestions for fixing the flaw

According to Golding,
the messages in the results are a requirement in SARIF.
But ["a good message](https://github.com/microsoft/sarif-tutorials/blob/main/docs/3-Beyond-basics.md#more-about-messages)
not only explains what was wrong:
it also explains why the flagged construct is considered questionable,
provides guidance for remedying the problem,
and explains when it's ok to ignore the result."
Regarding the levels of seriousness of the results,
in SARIF,
we typically see the values "error," "warning" and "note."
These values allude to problems ranging from severe to minor
(or simple opportunities to improve the code).
The locations,
on the other hand,
are optional since their being reported will depend on each case.
For instance,
[following Golding](https://github.com/microsoft/sarif-tutorials/blob/main/docs/2-Basics.md),
if a tool gives you the result
that your C# program doesn't have a `Main` entry point,
it would not have to mention a specific location.

This is just a glimpse of what you might discover in a SARIF file.
(By the way,
[on the SARIF website](https://sarifweb.azurewebsites.net/),
you can upload,
view and explore your SARIF files.)
Relying on this common format
when using multi-vendor tools for your software assessment
can undoubtedly mean time and effort savings
as well as better comparison and analysis of the results.
Results that you receive,
needless to say,
to improve the quality and security of your software.

An increasing number of companies are joining OASIS Open
to contribute to generating creative ideas
in favor of more secure software development.
As mentioned above,
there has been a whiff of a transformation of this standard since last year.
Cartey and Keaton,
OASIS SARIF TC co-chairs,
recently said that
["The next major version](https://www.oasis-open.org/2022/05/31/influx-of-cybersecurity-leaders-sign-on-to-support-new-version-of-oasis-sarif-standard-for-detecting-software-vulnerabilities/)
of SARIF will expand our ability
to aggregate data and detect vulnerabilities in some exciting new ways.
We look forward to the contributions of the companies that are joining now,
and we welcome others."

If what you want is a broad introduction to SARIF,
we invite you to review [the aforementioned tutorial](https://github.com/microsoft/sarif-tutorials/tree/main/docs).
For the complete documentation,
you can visit [SARIF's repository on GitHub](https://github.com/oasis-tcs/sarif-spec).
