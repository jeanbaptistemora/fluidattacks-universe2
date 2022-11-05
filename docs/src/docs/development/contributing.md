---
id: contributing
title: Contributing
sidebar_label: Contributing
slug: /development/contributing
---

Please submit bug reports,
feature requests,
or general feedback to our [Bug Tracker on GitLab](https://gitlab.com/fluidattacks/universe/-/issues),
or to our [Support Email](mailto:help@fluidattacks.com).

Since most of the contributions made to the project are code,
from now on this document explains the code contributions process.

## Steps

Code contributions are done using the Merge Requests features on GitLab.

As the Author of the contribution,
please read the following steps
and apply them in your day to day:

1. Make sure you have a working [Development Environment](/development/setup/environment).

1. Make sure that your contribution has an associated issue in the bug tracker,
   or create one.

   1. Make sure that you understand the motivation behind the issue,
      the problem it is trying to solve,
      its impact, its trade-offs,
      and that it makes sense to implement it as described.

      Issues are not set in stone,
      make sure you iterate on this as many times as needed,
      and edit the issue as you go.

   1. Make sure you enumerate all of the [products](/development/products)
      that will be impacted by the issue.

   1. Make sure the issue has received sufficient feedback from the Code Owners
      of the products impacted by the issue
      before starting any implementation.

   1. Don't be afraid to ping the author or the Code Owners for clarification.
      Excellent developers do excellent
      [requirement analysis](https://en.wikipedia.org/wiki/Requirements_analysis).

1. Code, and:

   1. For each of the issue's impacted products
      and their corresponding [product page](/development/products):

      1. Keep their docs updated.
      1. Make sure you follow their guidelines.
      1. Make sure you don't violate their Public Oaths.
      1. Keep their architecture updated.
      1. Add any missing information to their documentation.
         We want to be able to level up and empower other developers
         to write code autonomously and with confidence,
         but we cannot do so without documentation,
         [documentation is important](https://dilbert.com/strip/2007-11-26),
         make yourself [replaceable](https://betterprogramming.pub/programmers-make-yourself-replaceable-1b08a94bf5).

   1. Make sure that your implementation is sufficiently tested:

      1. By adding automated tests to the CI/CD.
      1. By manually testing the functionality.

      Feel free to use feature flags if appropriate.

   1. Make sure that you update the [End User documentation](/),
      particularly the [Machine](/machine/web/arm) section.

   1. Make sure that your implementation follows the general guidelines:

      1. [The licensing and copyright guidelines](/development/licensing-and-copyright).
      1. [The writing guidelines](/development/writing).

1. Open a [Merge Request](https://gitlab.com/fluidattacks/universe/-/merge_requests),
   and feel free to ping,
   assign,
   or send a direct message with the link
   to the Code Owners of the issue's impacted products.

1. Go back to step 3 until the issue is completed.

## Legal

:::tip
If you are a Fluid Attacks employee, you can skip this section,
since you have already signed a
[Contributor License Agreement](https://en.wikipedia.org/wiki/Contributor_License_Agreement)
as part of your employment contract.
:::

1. All of the code that you submit to our code repository
   will be licensed under the [MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/).
1. By submitting code to our code repository
   you also certify that you agree to the following
   [Developer Certificate of Origin](https://developercertificate.org/).

## Review process

We conduct code reviews using the Merge Requests features on GitLab,
and discussions should happen in the open,
either on the Issue,
the Merge Request,
or the team-wide communication channel.

Reviewers are selected by the Head of Product
and in general,
a reviewer reads the code,
reads the issue,
and then reviews the modified files by the Author.

A reviewer must have the following mindset
when performing a review:

1. **Transferring knowledge to the author**.

   This can range from a small code suggestion
   on how to make the code more maintainable or faster,
   to suggesting a library,
   reminding them of the guidelines,
   suggesting a way to organize the code,
   or signaling fundamental architecture/bugs/security problems
   that should be considered
   with the current approach the author is taking.

   [There are 8 quality characteristics of good software](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010).
   Help the author think about all of them.

1. **The author probably knows more than the reviewer**.

   The author is the one in the field,
   touching the code,
   and seeing the problem first-hand.
   Always give the benefit of the doubt
   and start the discussion with a question,
   rather than an affirmation that things are wrong.
   There is a chance the reviewer is not seeing the full picture.

1. **Neither the reviewer nor the author has more authority**.

   We are all [Developers](/development/governance).

   When proposing something make it sound like a proposal
   and not like an order.
   If what a reviewer says has value,
   the author will probably accept it and apply it right away.
   If a discussion arises,
   keep it healthy, constructive, and argument based.
   Either the author is seeing something the reviewer doesn't see yet
   or maybe the reviewer is seeing something the author doesn't see yet.
   This ["aha" moment](https://www.wordnik.com/words/aha%20moment)
   unlocks learning,
   and a safe environment to argue is key to good decision making.

1. **Minor improvements or fixes can come later**.

   If merging a Pull Request adds more value
   than closing it,
   go ahead and merge it.
   Just take note somewhere so that the author reminds amending it later.
   Also don't be too picky,
   specially about things that are subjective like style, formatting,
   or those that are too minor
   to even pay attention to (like a typo in a comment).

<!--
OpenSSF requirements:
How code review is conducted, what is checked, what is acceptable.
-->
