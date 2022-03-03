---
id: slb
title: Semantic Line Breaks
sidebar_label: Semantic Line Breaks
slug: /development/writing/slb
---

Our texts in the lightweight markup language
[Markdown](https://daringfireball.net/projects/markdown/)
*must* have Semantic Line Breaks (SLBs).
Acting as semantic delimiters,
SLBs reflect the logical structure of the writing,
facilitate the identification of grammatical errors
and the correction of the texts,
and help keep an organized record of modifications
in our version control system ([Gitlab](/development/stack/gitlab)).
Based on [sembr.org](https://sembr.org/),
we apply the following rules:

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

**Tip:** ["Try reading the text](https://sembr.org/) out loud,
  as if you were speaking to an audience.
  Anywhere that you pause for emphasis
  or to take a breath
  is usually a good candidate for a semantic line break."

Example:

![SLBa](https://res.cloudinary.com/fluid-attacks/image/upload/v1624062464/docs/development/writing/slba_x3kztj.webp)

For more information regarding SLBs and their use,
please check out the posts "[Semantic Linefeeds](http://rhodesmill.org/brandon/2012/one-sentence-per-line/)"
and "[Semantic linewrapping](https://scott.mn/2014/02/21/semantic_linewrapping/)."
