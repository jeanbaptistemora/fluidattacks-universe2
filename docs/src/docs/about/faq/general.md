---
id: general
title: General
sidebar_label: General
slug: /about/faq
---

## What is the Squad Plan?

The Squad Plan is a security testing service
that allows the hacking process
to begin at an early stage
in the software development cycle.
Its purpose is to guarantee **100% testing coverage**
of the application.

## What are the benefits of the Squad Plan?

The Squad Plan offers [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/),
a service with the following benefits:

- Minimizes the cost of remediation (repair)
  of a vulnerable security risk
  while the software is in development
  rather than when it is in production.

- Reduces application certification time to zero
  because the hacking is done during development.

- Provides clear and detailed information
  about vulnerable security risks
  and facilitates a coordinated effort
  between external project personnel
  (`Fluid Attacks` experts)
  identifying security risks
  and internal project personnel
  (client company)
  fixing security issues without delays.

## In what industries does your company have experience?

Throughout our trajectory
we have been working with companies from different sectors,
such as finance, transportation,
industry, consumer, communications,
technology and utilities.

## Is it possible to hire an On-the-Premises Squad Plan?

No.
Due to the operational model
behind the Squad Plan,
it can only be done remotely.

## At 100% coverage, is the Squad Plan suspended until new changes are added?

No.
Even if 100% of coverage is reached,
we continue checking already attacked source code
to identify any possible false negatives,
including components developed by third parties
in our hacking process.

## When does the Squad Plan end?

The Squad plan is contracted for a minimum of **12 months**
and is renewed automatically
at the end of the 12-month period.
The Squad Plan ends
when we receive a written request
through previously defined channels
to terminate the contract.

## Can the contract be canceled at any time?

You can cancel your contract
at any time after the fourth month.
Cancellation can be requested
through any communication channel
previously defined in the contract.

## Can the Squad Plan be used for code developed a long time ago?

Yes,
it is still possible to use the Squad Plan.
There are two options available:

- A Health Check can be performed
  that tests all existing code.
  Then,
  the Squad Plan is executed as usual
  within the defined scope
  (see [this question](/about/faq/speed#how-are-development-cycles-not-slowed-down-by-manual-reviews)).
  This option is better suited
  for applications under development.

- Start with the standard limits
  (see [this question](/about/faq/speed#does-the-squad-plan-use-automated-tools-or-is-it-a-manual-process)),
  increasing the coverage
  on a monthly basis
  until 100% is reached.
  This option is better suited
  for applications
  that are no longer in development.

## Can you review all the existing code before starting the tests?

We recommend
that application development
and the hacking process
begin simultaneously.
However,
this is not always possible.
To catch up with developers,
we perform a Health Check
(additional fees apply).
This means
all versions of the existing code are attacked
up to the contracted starting point
in addition to the monthly test limit.
This allows us to catch up
with the development team
within the first **three contract months**.
Then,
we continue hacking simultaneously
with the development team
as development continues.

## What if I want the Squad Plan but not the Health Check?

This is a risky choice.
Not performing a Health Check
means there will be code
that is never going to be tested
and, therefore,
it's not possible to know
what vulnerabilities may exist in it;
those vulnerabilities will not be identified.
We guarantee that
**100% of the code change** will be tested,
but what cannot be reached,
cannot be tested.

## With the Squad Plan, can I include the infrastructure of my app?

We have improved the Squad Plan model
to now include infrastructure
within the Target of Evaluation (ToE).
This includes the application's ports,
inputs, infrastructure,
and of course
the application itself.

## What external tools do you use to perform pentesting?

We use [Burp Suite](https://portswigger.net/burp) for web testing,
and [CANVAS](https://www.immunityinc.com/products/canvas/)
and [Core Impact](https://www.coresecurity.com/products/core-impact)
for infrastructure testing
with additional exploits.

## Where does ASM run?

Our [ASM](https://fluidattacks.com/categories/asm/) (Attack Surface Manager) platform
runs in the cloud.

## Do you manage the access credentials to ASM?

No.
We use federated authentication.
Google, Azure (Microsoft 360) and Bitbucket are the entities
that validate your user access credentials.

## Can I activate the double authentication token?

Yes,
you can,
and we recommend you do so.
Using double authentication will increase the security level
of your credentials.
This will help prevent unauthorized users
from accessing and compromising your information.
This feature is enabled
through Gmail or Azure.

## How will our data be stored?

We store data on AWS in the cloud
(mainly S3 and DynamoDB, all security enabled)
and on hackers' computers
with disk encryption in all partitions.
On [this page](/about/security/confidentiality/encryption-rest)
you can read
how we ensure the confidentiality of our clients' data.

## How will our data be transmitted?

It is up to you.
However,
we recommend the use of HTTPS
for application tests
and SSH (git)
for source code analysis.

## What retesting options are available?

[One-Shot Hacking](https://fluidattacks.com/services/one-shot-hacking)
includes one retest.
The Squad Plan
([Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/))
includes infinite retests
during the subscription time.

## Can I recognize the vulnerabilities of multiple apps in one subscription?

According to the active authors model,
it is possible to create a large cell
with all the developers
or to divide it into applications
according to the client's needs.
When managing only one cell,
it is important to consider the following:

- All users in the project
  can see all the vulnerabilities of the application
  inside the same cell.
- When the same vulnerability appears in several applications,
  the only way to identify/locate each one
  in each individual application
  is by checking the vulnerability report
  under the heading "location."
  There,
  it will specify
  where each vulnerability can be found.

## Can I change the environment when the subscription is already active?

Yes,
you can,
under the condition
that the new environment be the same branch environment
where the source code is reviewed,
thus allowing us to test the same version of the change
both statically and dynamically.

## How do you ensure the availability of my apps while you test them?

It is possible to cause an accidental DoS
during the hacking service.
We recommend including only the staging phase
in the scope.
However,
many clients decide to also include the production stage
in the tests.
It is unusual for us
to take down environments
because when we foresee a possible breakpoint,
we ask the client for a special environment
to carry out the test.

## What happens if I want to review different environments of the same app?

The service includes the environment of the reviewed code.
It is possible to include different environments
for an additional fee.

## Severity vs. vulnerabilities

The analysis that groups the number of vulnerabilities
has the following problems:

- Not all the vulnerabilities
  have the same severity (CVSS).
- A vulnerability with a severity of 10
  is not equal to two vulnerabilities
  with a severity of 5.

Grouping vulnerabilities by ranges
(low, medium, etc.)
presents the same problems by segments
as well as additional ones:

- A vulnerability of 9.9 is not 10% more severe
  than a 9.0 (i.e., critical).
- **Arbitrariness** in the segmentation:
  8.9 is not critical, but 9.0 is?
- Increases **complexity**:
  four non-groupable data sets
  instead of one.

For these reasons,
executive analysis based on vulnerability grouping,
either without or with ranges,
is not recommended.

## Adjustment by severity

A **4 ^ (CVSS - 4)** severity adjustment is recommended
to allow the grouping of vulnerabilities.
It reflects the exponential nature of the severity
in each vulnerability:

1. Reduces the severity of vulnerabilities:

  a. Little severe

  b. Very frequent

1. Increases the severity of vulnerabilities:

  a. Highly severe

  b. Infrequent

1. Allows:

  a. Analysis aggregated into a single data set

  b. No arbitrary ranges

  c. Reality aligned **prioritization**

## Adjustment by severity: equivalences

![cvss-table.png](https://res.cloudinary.com/fluid-attacks/image/upload/v1627330928/docs/about/faq/cvss-table_dzfa1h.png)

Examples:

- The table shows that
  vulnerability 10 (row) equals
  262,144 vulnerabilities 1 (column).
- A vulnerability 5 (row)
  equals 16 times the severity
  of a vulnerability 4 (column).
