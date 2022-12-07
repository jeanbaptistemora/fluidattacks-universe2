---
id: merge-request
title: Merge Request
sidebar_label: Merge Request
slug: /development/stack/commitlint/syntax/merge-request
---

## Differences with commit messages

Merge Request commits
are like commit messages
with only three differences:

1. Merge Request [type]
   has to be the most relevant type
   of all its commits.
   The relevance list is:

   ```markup
   rever
   feat
   perf
   fix
   refac
   test
   style
   sol
   ```

   Where `revert`
   has the highest
   and `sol`
   the lowest relevance.

   For example,
   if your MR has one `feat`,
   one `test`
   and one `style` commit,
   the [type] of your MR
   must be `feat`.

1. They **can** (not mandatory) implement
   a `Closes #{issue-number}`
   in their footer,
   which triggers the automatic closing
   of the referenced issue
   once the MR gets accepted

## Merge Request example

Here is an example
of a compliant Merge Request Message:

```markup
integrates\feat(build): #13 new checks to dangerfile

- Add type_check
- Add deltas_check
- Add commit_number check

Closes #13
```

Issue number 13
will be automatically closed
once this MR is accepted
due to the `Closes #13` footer.

## ETA Merge Request messages

When your Merge Request
is related to one area/issue
that has an enumerable universe,
i.e,
we know with considerable certainty
how many MRs are necessary
to complete it,
then you should use
the following ETA model
as a Merge Request message:

```markup
- Speed: A [parts] / B [time unit] = A/B [parts]/[time unit]
- TODO: C [parts]
- ETA: C / (A/B) = C/(A/B) [time unit]
```

[**parts**] should be replaced for
the aspect that allows to
quantify the progress of the area,
which can be a number of issues,
cases, files, tasks, etc.

[**time unit**] should be replaced for
an appropiate unit of time
that will be used to estimate an ETA,
for example days or weeks.

**B** is the units of time that has passed
since you started addressing
the issues of the area,
**A** is the total number of [**parts**]
that have been submitted in such **B** time
and **C** is the total number of [**parts**]
that we know will resolve the issues of the area.

ETA Merge Request message example:

```markup
- Speed: 4 issues / 2 days = 2 issues/day
- TODO: 10 issues
- ETA: 10 / 2 = 5 days
```
