---
id: exclusions
title: Exclusions
sidebar_label: Exclusions
slug: /machine/web/groups/scope/exclusions
---

There are cases
when it is necessary
to exclude a number of files
or whole folders
from the scope
of the tests we perform.
There are many reasons
why you may want to do this,
maybe you want to exclude
the many functional tests
that your repository has,
exclude some dummy files
that you haven't deleted,
etc.,
the circumstances are varied.
The ASM gives you a way to do this,
however,
remember that any files or folders
excluded by the gitignore
will prevent any more vulnerabilities
from being reported for them
and are effectively taken out
of the scope of the group,
so we advice you
to be careful with this.

## How to exclude paths from the scope of my group?

In order to do this,
we have a section
that appears
when you are adding or editing
a git root in your group.

![Git Root Buttons](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211880/docs/web/groups/scope/git_root_buttons_pviqnf.webp)

You just need to go
to the scope section of your group
and click on the **Add new root**
or **Edit root** button
depending on what you want to do,
and a window will show up.

There you can see
the section that says **Gitignore**,
this is where you can specify
the paths that you don't want us to test.
Here you can click
on the **plus(+)** sign
to start adding **patterns**
for the files and/or folders
you want to exclude.
In case you are wondering
what is this **pattern**
we are talking about,
you can also click
on the **interrogation sign(?)**
besides the word **gitignore**
to access a web page
that instructs you on how to write it.
For your convenience,
you can also click
[this link](https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitignore.html#_pattern_format)
to access said web page.
Using these **patterns**
you can efficiently exclude
all the files and folders you want,
however,
we advice you to be careful
when you use the **wildcard(*)**,
as this may cause you to accidentally exclude
something you don't want to
and stop receiving reports
of any vulnerabilities in it,
so whenever you can,
always try to be specific
when excluding paths.

## Examples

Here we have some examples:

- node_modules/
- build/tmp/
- test/*.js (Here we use the wildcard that we advised you to be careful with)
- repo-root/dummy/excludeme.js

> **Note:** This subsection is pending review.
> Some of the information might be outdated.
