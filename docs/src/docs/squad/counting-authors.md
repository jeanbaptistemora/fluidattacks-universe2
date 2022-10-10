---
id: counting-authors
title: Billing author count
sidebar_label: Billing author count
slug: /squad/counting-authors
---

Squad Plan billing for an
organization is based on
the number of [active monthly authors](/about/faq/billing/#does-the-cost-vary-according-to-the-scope-or-development-phases)
(developers) contributing
to its code repositories.
To count these authors,
we check the commits recording
changes made to the code
repositories and integrated
to the branch under continuous
hacking during a month.

First,
we extract metadata of commits
made and store it in an
append-only database.
Next,
we add the dates on which we
first found these commits.
Then,
we filter them for a specific
month and make adjustments to
remove duplicate authors.
We know that an author might
have used other accounts to
make some commits in addition
to those made using their
primary email/account.
The resulting list is what we
use to calculate the billing
for the organization in a given month.

Our customers can check these
lists of active monthly authors
any time they want in the
[Authors section](/machine/web/groups/authors/)
of each group in the ARM.
These lists include the names
of the authors and the groups to
which they have contributed,
the commit IDs
(a single example per author)
and the repositories’ names.
