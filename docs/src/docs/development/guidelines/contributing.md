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

## Code contributions

### Checklist

1. Make sure that your contribution has an associated issue in the bug tracker,
   or create one.

   1. Make sure that you understand the motivation behind the issue,
      the problem it is trying to solve,
      its impact, its trade-offs,
      and that it makes sense to implement it as described.

      Issues are not set in stone,
      make sure you iterate on this as many times as needed,
      and to edit the issue as you go.

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

1. Go back to step 2 until the issue is completed.

### Legal

:::tip
If you are a Fluid Attacks employee, you can skip this section.
:::

1. All of the code that you submit to our code repository
   will be licensed under the [MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/).
1. By submitting code to our code repository
   you also certify that you agree to the following
   [Developer Certificate of Origin](https://developercertificate.org/).
