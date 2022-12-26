---
id: hacking-our-technology
title: Continuous Hacking to Our Technology
sidebar_label: Continuous Hacking to Our Technology
slug: /about/security/transparency/hacking-our-technology
---

We have projects focused
on hacking our software.
It is essential for us
to be an example of secure software.
That's why
our entire technology stack
goes through a process
of comprehensive
[Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/).

All our development projects run
[Continuous Integration](https://docs.fluidattacks.com/about/security/integrity/developing-integrity#continuous-integration)
pipelines,
including exploits and strict linters,
to ensure that
[no known vulnerabilities](/criteria/requirements/155)
are released to production.

Additionally,
we run [a bug bounty program](https://www.openbugbounty.org/bugbounty/fluidattacks/)
to ensure the highest security
and privacy of our websites.
Everyone is eligible to participate in the bug bounty program,
and people is encouraged to find
and responsibly report vulnerabilities
through a monetary award
based on the impact of the vulnerability.

## Vulnerability Response Process

1. Researcher submits a report
   through any of the channels mentioned above.

1. A Response Team is assigned,
   based on availability and the knowledge-set.

1. Response Team responds to Researcher.
   and makes inquiries
   to satisfy any needed information
   and confirm if the report is indeed a vulnerability.
   If it is not a vulnerability,
   the Response Team communicates to Researcher why.

1. A severity of the vulnerability is established
   based on its [CVSS](https://www.first.org/cvss/) score.

1. A confidential issue is created in
   [Fluid Attacks' bug tracker](https://gitlab.com/fluidattacks/universe/-/issues),
   and prioritized according to its severity.

   If appropriate,
   users are notified of the vulnerability
   including any steps for them to take,
   but without any details
   that could suggest an exploitation path.

1. Appropriate patches are worked on locally
   by the Response Team.

1. Patches are reviewed with the researcher.

1. Vulnerability announcement is drafted
   and a release date if discussed.

1. At the release date:
   the fix is deployed,
   and the vulnerability is announced at [Fluid Attacks News](https://news.atfluid.com/),
   and through e-mail to the affected users if appropriate.

1. The researcher is contacted and asked if they wish for credit.

1. Internal Fluid Attacks meetings are held
   in order to analyze the incident
   and take any actions that can isolate our code base,
   prevent similar incidents,
   reduce future incidents,
   or improve future responses.

## Requirements

- [155. Application free of malicious code](/criteria/requirements/155)
