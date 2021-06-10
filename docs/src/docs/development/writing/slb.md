---
id: slb
title: Semantic Line Breaks
sidebar_label: Semantic Line Breaks
slug: /development/writing/slb
---

Our texts in [Markdown](https://daringfireball.net/projects/markdown/)
and [AsciiDoc](https://asciidoc.org/) *must* have Semantic Line Breaks (SLB)
to facilitate editing and help keep an organized record of modifications
in our version control system ([Gitlab](https://gitlab.com/)).
Based on [sembr.org](https://sembr.org/), we consider the following rules:

* An SLB *should not* alter the intended meaning of the text.

* An SLB *must* occur after a sentence,
  which ends with a period, exclamation mark or question mark.

* An SLB *should* occur after an [independent clause](https://www.grammar-monster.com/glossary/independent_clause.htm)
  that is punctuated by a comma, semicolon, colon, or em dash.

* An SLB *may* appear after a [dependent clause](https://www.grammar-monster.com/glossary/dependent_clause.htm)
  to clarify grammatical structure or satisfy line length restrictions.

* An SLB is *recommended* before an itemized or enumerated list.

* An SLB *may* be used after one or more items in a list
  to logically group related elements or satisfy line length restrictions.

* An SLB *must not* occur within a hyphenated word.

* An SLB *may* occur before and after a hyperlink.

* An SLB *may* occur before [inline markup](https://docutils.sourceforge.io/docs/user/rst/quickref.html#inline-markup).

* The maximum number of characters before an SLB *must* be 80,
  except in cases with hyperlinks or code elements.

> **NOTE:**
> This section of our documentation is under construction.
