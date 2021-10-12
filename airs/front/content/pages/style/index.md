---
slug: style/
title: Writer’s Guidelines
description: Learn the acceptance criteria, the format and structure requirements, and all the main guidelines to publish articles and documents on our website.
keywords: Fluid Attacks, Style, AsciiDoc, Articles, Requirement, Website, Guidelines, Writer's Guidelines, Ethical Hacking, Pentesting
category: blog
---

Our target audience is everyone with an interest in `IT` security,
whether they have advanced technical knowledge or not. We suggest to use
as much non-technical English as possible. It is always best to be
clear, concise, and to-the-point.

## Topics

Check our [list of topics](../topics/).

## Acceptance Criteria

### 1\. Title

The title of the article must grab the reader’s attention. **It must not
exceed 35 characters**

1.  Make the topic something fun or interesting. It can be in the form
    of a question.

    **Examples:**

      - Wanting the `Cookie`.

      - Information Security, an expense or an investment?

2.  Absolutely no generic titles.

    **Examples:**

      - SQL Injection.

      - XSS Vulnerability.

### 2\. Structure

The document must have a `LIX` complexity **below 50**. This guarantees
that the document is easy to read. All documents must have:

1.  An introduction that tells the reader what your article is about and
    what they can expect.

2.  A body containing specific information (details) that supports or
    elaborates on your introduction.

3.  A short conclusion that wraps up or restates the important points
    from the introduction.

### 3\. Format

Documents will only be accepted in an `AsciiDoc` format. For more
information check out our [format page](../format/), the [`AsciiDoc`
guide](http://AsciiDoctor.org/docs/AsciiDoc-writers-guide/), or a [quick
reference](http://AsciiDoctor.org/docs/AsciiDoc-syntax-quick-reference/).

### 4\. Word limit

Documents have strict length limits:

1.  **For Posts:** between `800` and `1200` words.

2.  **For pages (sites):** Between `400` and `1200` words.

### 5\. Semantic Line Breaks

Documents must have Semantic Line Breaks ([SLB](http://sembr.org/)), in
order to facilitate editing and keep an organized record of
modifications in our version control system (`Gitlab`). To do this, we
define the following rules:

1.  Minimum words before a SLB: `4`.

2.  Maximum number of characters before a SLB: `80`.

3.  A SLB **must** be added after a period (.).

4.  A SLB **can** be added after [linking words and
    connectors](https://emedia.rmit.edu.au/learninglab/content/common-linking-words-0),
    depending on the context and respecting the previous rules.

Exceptions to the rule are:

1.  Links.

2.  Source Code.

**Example:**

<div class="imgblock">

![SLB
Example.](https://res.cloudinary.com/fluid-attacks/image/upload/v1620242348/airs/style/slb-example_qacz6k.webp)

<div class="title">

Figure 1. SLB Example.

</div>

</div>

For more information regarding `SLB` and their use, you can check out
the [semantic linefeeds
guide](http://rhodesmill.org/brandon/2012/one-sentence-per-line/),
[semantic line wrapping
guide](https://scott.mn/2014/02/21/semantic_linewrapping/), or the
[`AsciiDoc`
documentation](http://AsciiDoctor.org/docs/AsciiDoc-recommended-practices/#one-sentence)

### 6\. Images

1.  All documents must include at least one image related to the topic
    being presented.

2.  All documents covers must be from [unsplash](https://unsplash.com/).

3.  All documents must include at least one image from
    [unsplash](https://unsplash.com/) and ideally another graphic
    reference (it can be from [unsplash](https://unsplash.com/) or any
    other webpage).

4.  Use free professional images from [unsplash](https://unsplash.com/).

5.  Images that are not yours must include a reference.

6.  Include a description of the image.

### 7\. Source

Unless the language forces you to do otherwise, the source code must
comply with the following:

1.  Be in English (even the comments).

2.  Indent using `2` spaces instead of tabs, unless the language
    requires otherwise.

3.  Use the `brace style` seen in
    [stroustrup](https://en.wikipedia.org/wiki/Indentation_style#Variant:_Stroustrup)
    (`no one liners`).
    [Example](https://eslint.org/docs/rules/brace-style#stroustrup).

4.  Lines must not exceed `80` characters in length.

5.  Lines must not contain [`debug`
    comments](https://en.wikipedia.org/wiki/Comment_\(computer_programming\)#Debugging)
    left behind.

6.  Function definition must be separated by `1` empty line, unless the
    linter or the language requires otherwise.

Embedded code snippets must comply with the following:

1.  Be enumerated. To do so add the parameter `linenums` to the `source`
    block.

2.  Not have more than `8` lines.

3.  No repeating a snippet that has already been used in the guide.

4.  Add the lines of code to the `post` using a code block, don’t use
    images.

**Example:**

**example.c.**

``` C
function cool(x) {
  /*Please use SHORT comments in english when necessary.
  You must explain your code in the document*/
  int y;
  y = x + 1;
  return y;
  //And remember, do NOT exceed 8 lines ;)
}
```

### 8\. Exploit Explanations

In the case of documents focused on exploitation, once the procedure is
explained, we recommend including a short `gif` showing the result of
what was explained. Add a description for the `gif`.

<div class="imgblock">

![Exploit description
example.](https://res.cloudinary.com/fluid-attacks/image/upload/v1620242348/airs/style/exploitation_z4npfw.gif)

<div class="title">

Figure 2. Exploit description example.

</div>

</div>

### 9\. Not permitted

1.  Code snippets that are not your own.

2.  Technical explanations not relevant to security:

    **Example:** Introduction to a programming language without
    mentioning how to securely program in said language.

### 10\. Metadata

Metadata are variables which influence the final rendering of the pages
and how the search engine indexes them. Below is a table with the
mandatory metadata for a document:

<div class="tc">

**Table 1. List of metadata present in a document.**

</div>

| **Metadata**         | **Page**     | **Post**     | **Description**                                                                                                                                                                                                        |
| -------------------- | ------------ | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `:page-slug:`        | <p> Yes </p> | <p> Yes </p> | <p> Link where the document can be found once it has been accepted. The `slug` must be the name of the article in lowercase, with no spaces, prepositions, conjunctions or connectors and separated by a dash "-".</p> |
| `:page-description:` | <p> Yes </p> | <p> Yes </p> | <p> Brief summary of the main idea of the document (**250 to 300 characters long**). This description will appear in the search engine search results. </p>                                                            |
| `:page-keywords:`    | <p> Yes </p> | <p> Yes </p> | <p> Keywords through which a search engine can find the document. The document must include 6 `keywords`. </p>                                                                                                         |
| `:page-subtitle:`    | <p> Yes </p> | <p> Yes </p> | <p> Short subtitle that specifically indicates the purpose of the document. **It must not exceed 55 characters**. </p>                                                                                                 |
| `:date:`             | <p> No </p>  | <p> Yes </p> | <p> Date the document was created. </p>                                                                                                                                                                                |
| `:category:`         | <p> No </p>  | <p> Yes </p> | <p> Category to which the document falls under. Example: Security opinions, Best practices, etc.   </p>                                                                                                                |
| `:tags:`             | <p> No </p>  | <p> Yes </p> | <p> Similar to the metadata `:page-keywords:` Noteworthy words that index the document internally. </p>                                                                                                                |
| `:image:`            | <p> No </p>  | <p> Yes </p> | <p> Image that will appear in the article preview. This image must have certain dimensions, 900 x 600 px and must not exceed 800 Kb in size. </p>                                                                      |
| `:alt:`              | <p> No </p>  | <p> Yes </p> | <p> Description of the image in the article preview. </p>                                                                                                                                                              |
| `:author:`           | <p> No </p>  | <p> Yes </p> | <p> Name of the author that will appear at the top of the document. Name and last name only. </p>                                                                                                                      |
| `:writer:`           | <p> No </p>  | <p> Yes </p> | <p> Name and extension of the image that represents you as the author. The only extension permitted is `PNG`. </p>                                                                                                     |
| `:name:`             | <p> No </p>  | <p> Yes </p> | <p> Name that will appear under the author’s image/picture. It can be your full name or `nickname`. </p>                                                                                                               |
| `:about1:`           | <p> No </p>  | <p> Yes </p> | <p> Main information about the author: scholarship, experience, role (if it applies). </p>                                                                                                                             |
| `:about2:`           | <p> No </p>  | <p> Yes </p> | <p> Additional information about the author: likes, interests, links to personal blogs or profiles. </p>                                                                                                               |
| `:source:`           | <p> No </p>  | <p> Yes </p> | <p> Link to the cover image from [unsplash](https://unsplash.com/). </p>                                                                                                                                               |

### 11\. Additional Information

1.  If acronyms are used, their meaning should be included in
    parentheses.

2.  Include references when using fragments from external sources.

3.  Paragraphs **must** be original; don’t use text from other sites
    unless they are specific phrases.

4.  Foreign and reserved words used outside of blocks of code must use
    `monospace`.

5.  Make sure to include the `link:` before adding a link.

6.  When writing the company name (`Fluid Attacks`), consider the
    following cases:

      - **Case 1:** If the name is placed next to the company logo, it
        must be written as follows:

        <pre>
         ___
        | >>|> fluid
        |___|  attacks

        </pre>

      - **Case 2:** If the name is used as part of a domain, `URL` or
        file path, it must be written in lowercase without spaces:

        <pre>

        path/fluidattacks/file

        www.fluidattacks.com

        </pre>

      - **Case 3:** In any other case, it must be written in Title Case
        and separated:

        <pre>

        Fluid Attacks: We hack your software, zero false positives

        </pre>

7.  When including a reference, use the letter "r" as an `anchor_ID`
    followed by the reference number. Use superscript to quote it.

**Example:**

<pre>

I'm talking about some topic
and now I need to cite a reference <<r# ,^[#]^>>

== References

. [[r#]] link:https://my-url[Fancy name for url].

</pre>

## Authors

**Do not forget** to send with it a paragraph telling us a little bit
about yourself and an image that represents you because at the end of
the post the authors’s profile will be included.

<div class="imgblock">

![guest](https://res.cloudinary.com/fluid-attacks/image/upload/v1620242347/airs/style/guest_etlyxo.webp)

</div>

1.  Author’s first and last name.

2.  Short description, minimum 15 words – maximum 30. You may include:
    What you do for a living, years of experience, certifications, likes
    and interests.

3.  Optional: Link to personal blog – `github` – `linkedin`

### Requests

If you are not part of the `Fluid Attacks` team, you just have to send
your document to <communications@fluidattacks.com> attaching all the
required files in order to create the `post`. Once the document is sent,
it is evaluated to determine if it will be published.

## Terms and Conditions

1.  `Fluid Attacks` reserves the right to accept or reject any document
    sent in. `Fluid Attacks` does not pay for articles accepted for
    publication on the blog.

2.  We perform a non-substantive review of the document. `Fluid Attacks`
    doesn’t evaluate if we agree or not with the author’s opinion as
    expressed in the document, but only that the document meets the
    required criteria described above.

3.  Once a draft is completed you must request the revision of the
    document through a `Merge Request` so that we can evaluate the
    content.

If the document is accepted and published, the author retains the
copyright to the draft submitted to `Fluid Attacks`. However, `Fluid
Attacks` **retains** the right to make changes to the draft, if
necessary, and these may be made without the author’s consent or
notification.
