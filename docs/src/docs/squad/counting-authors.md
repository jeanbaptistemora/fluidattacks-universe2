---
id: counting-authors
title: Counting Authors
sidebar_label: Counting Authors
slug: /squad/counting-authors
---

For us to calculate the billing
of clients, we need to know how
many developers (authors) are
working on the application.
To find this out for each month,
we have a complete and reliable
process.

Everything begins when the developers
start making changes into the repository.
As we know, every time a change is
generated within the application,
**commits** are created in turn.
These are objects that save the
information about the change
that was made.

Fluid Attacks relies on a program
that can extract only the data of
commits created by the developers
and store them in an append only
database.
This database stores everything
that makes up a commit and adds
the date on which we first
find/visualize the commit.

On the database, we create a filter
to select only the commits created
during a specific month.
Having this filtered information, we
move on to adjusting per authors.

Such an adjustment has the purpose
of identifying the authors who use
**aliases**.
An alias is an alternate name that
developers use to shorten text.
We make the adjustment with
**mailmap**, which maps and scans
email addresses included in the commit.
By detecting aliases we can avoid
counting any author more than once.
After this adjustment, we export the
resulting database to our software
as a file and share it through the ASM.

At the end of this process, we get
a complete filename.
This file has the author name, email
address, group name, seen date, commit
and repository name.
Thanks to this process, we get the
content of authors on each group, which
is clear and concise information.
